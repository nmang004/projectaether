# Frontend Integration Guide for Project Aether API

## Table of Contents
1. [Overview](#overview)
2. [Setting Up API Client](#setting-up-api-client)
3. [Authentication Flow](#authentication-flow)
4. [Site Audit Integration](#site-audit-integration)
5. [AI Features Integration](#ai-features-integration)
6. [Error Handling](#error-handling)
7. [State Management](#state-management)
8. [TypeScript Types](#typescript-types)
9. [React Components Examples](#react-components-examples)

## Overview

This guide provides comprehensive instructions for integrating the Project Aether backend API with frontend applications. The examples use React with TypeScript, but the patterns can be adapted to other frameworks.

## Setting Up API Client

### Base API Configuration

Create a centralized API client to handle all HTTP requests:

```typescript
// src/services/api.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

export interface ApiConfig {
  baseURL: string;
  timeout?: number;
}

class ApiClient {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor(config: ApiConfig) {
    this.client = axios.create({
      baseURL: config.baseURL,
      timeout: config.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add authentication token
    this.client.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.clearToken();
          // Redirect to login or dispatch logout action
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  setToken(token: string): void {
    this.token = token;
    localStorage.setItem('auth_token', token);
  }

  clearToken(): void {
    this.token = null;
    localStorage.removeItem('auth_token');
  }

  loadToken(): void {
    const token = localStorage.getItem('auth_token');
    if (token) {
      this.token = token;
    }
  }

  async request<T>(config: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.request(config);
    return response.data;
  }
}

// Create API client instance
export const apiClient = new ApiClient({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
});

// Load token on app initialization
apiClient.loadToken();
```

## Authentication Flow

### Authentication Service

```typescript
// src/services/authService.ts
import { apiClient } from './api';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface User {
  email: string;
  full_name: string;
  id: string;
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await apiClient.request<AuthResponse>({
      method: 'POST',
      url: '/auth/login',
      data: credentials,
    });

    // Store the token
    apiClient.setToken(response.access_token);
    
    return response;
  }

  async register(userData: RegisterData): Promise<AuthResponse> {
    const response = await apiClient.request<AuthResponse>({
      method: 'POST',
      url: '/auth/register',
      data: userData,
    });

    // Store the token
    apiClient.setToken(response.access_token);
    
    return response;
  }

  logout(): void {
    apiClient.clearToken();
  }

  async getCurrentUser(): Promise<User> {
    return apiClient.request<User>({
      method: 'GET',
      url: '/auth/me',
    });
  }

  isAuthenticated(): boolean {
    return localStorage.getItem('auth_token') !== null;
  }
}

export const authService = new AuthService();
```

### React Authentication Hook

```typescript
// src/hooks/useAuth.ts
import { useState, useEffect, useContext, createContext } from 'react';
import { authService, User } from '../services/authService';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      if (authService.isAuthenticated()) {
        try {
          const userData = await authService.getCurrentUser();
          setUser(userData);
        } catch (error) {
          console.error('Failed to load user:', error);
          authService.logout();
        }
      }
      setIsLoading(false);
    };

    loadUser();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      await authService.login({ email, password });
      const userData = await authService.getCurrentUser();
      setUser(userData);
    } catch (error) {
      throw error;
    }
  };

  const register = async (email: string, password: string, fullName: string) => {
    try {
      await authService.register({ email, password, full_name: fullName });
      const userData = await authService.getCurrentUser();
      setUser(userData);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

## Site Audit Integration

### Audit Service

```typescript
// src/services/auditService.ts
import { apiClient } from './api';

export interface StartAuditRequest {
  root_url: string;
  max_depth?: number;
  max_pages?: number;
}

export interface AuditTask {
  task_id: string;
  status: string;
  message: string;
  root_url: string;
}

export interface AuditProgress {
  phase: string;
  progress: number;
  total: number;
  crawled?: number;
  current_url?: string;
}

export interface AuditStatus {
  task_id: string;
  status: 'PENDING' | 'PROGRESS' | 'SUCCESS' | 'FAILURE';
  result?: AuditResult;
  progress?: AuditProgress;
  error?: string;
  message: string;
}

export interface AuditResult {
  project_id: number;
  root_url: string;
  crawl_summary: {
    total_pages_crawled: number;
    total_pages_discovered: number;
    crawl_depth_reached: number;
    crawl_duration_seconds: number;
    crawl_status: string;
  };
  seo_metrics: {
    pages_with_missing_titles: number;
    pages_with_missing_descriptions: number;
    pages_with_duplicate_titles: number;
    pages_with_duplicate_descriptions: number;
    pages_with_missing_h1: number;
    pages_with_broken_links: number;
    average_page_load_time: number;
    pages_with_images_missing_alt: number;
  };
  technical_issues: {
    pages_with_4xx_errors: number;
    pages_with_5xx_errors: number;
    pages_with_redirect_chains: number;
    pages_with_large_dom: number;
    pages_with_render_blocking_resources: number;
  };
  performance_metrics: {
    average_first_contentful_paint: number;
    average_largest_contentful_paint: number;
    average_cumulative_layout_shift: number;
    pages_failing_core_web_vitals: number;
  };
}

export interface AuditHistoryItem {
  task_id: string;
  root_url: string;
  status: string;
  created_at: string;
  completed_at?: string;
  pages_crawled: number;
  issues_found: number;
}

export interface AuditHistory {
  audits: AuditHistoryItem[];
  total: number;
  limit: number;
  offset: number;
}

class AuditService {
  async startAudit(request: StartAuditRequest): Promise<AuditTask> {
    return apiClient.request<AuditTask>({
      method: 'POST',
      url: '/audits/start',
      data: request,
    });
  }

  async getAuditStatus(taskId: string): Promise<AuditStatus> {
    return apiClient.request<AuditStatus>({
      method: 'GET',
      url: `/audits/status/${taskId}`,
    });
  }

  async getAuditHistory(limit = 10, offset = 0): Promise<AuditHistory> {
    return apiClient.request<AuditHistory>({
      method: 'GET',
      url: '/audits/history',
      params: { limit, offset },
    });
  }
}

export const auditService = new AuditService();
```

### React Audit Hook

```typescript
// src/hooks/useAudit.ts
import { useState, useCallback } from 'react';
import { auditService, StartAuditRequest, AuditStatus } from '../services/auditService';

export const useAudit = () => {
  const [isStarting, setIsStarting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startAudit = useCallback(async (request: StartAuditRequest) => {
    setIsStarting(true);
    setError(null);
    
    try {
      const task = await auditService.startAudit(request);
      return task;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to start audit';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsStarting(false);
    }
  }, []);

  return {
    startAudit,
    isStarting,
    error,
  };
};

export const useAuditStatus = (taskId: string | null, pollingInterval = 5000) => {
  const [status, setStatus] = useState<AuditStatus | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const checkStatus = useCallback(async () => {
    if (!taskId) return;

    setIsLoading(true);
    setError(null);

    try {
      const auditStatus = await auditService.getAuditStatus(taskId);
      setStatus(auditStatus);
      return auditStatus;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to check audit status';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, [taskId]);

  // Auto-polling for status updates
  useEffect(() => {
    if (!taskId || !status || ['SUCCESS', 'FAILURE'].includes(status.status)) {
      return;
    }

    const interval = setInterval(checkStatus, pollingInterval);
    return () => clearInterval(interval);
  }, [taskId, status, checkStatus, pollingInterval]);

  // Initial status check
  useEffect(() => {
    if (taskId) {
      checkStatus();
    }
  }, [taskId, checkStatus]);

  return {
    status,
    isLoading,
    error,
    checkStatus,
  };
};
```

## AI Features Integration

### AI Service

```typescript
// src/services/aiService.ts
import { apiClient } from './api';

export interface KeywordClusterRequest {
  head_term: string;
}

export interface KeywordClusters {
  [cluster: string]: string[];
}

export interface KeywordClusterResponse {
  head_term: string;
  clusters: KeywordClusters;
  generated_by: string;
  user: string;
}

export interface SchemaMarkupRequest {
  content: string;
  schema_type: string;
}

export interface SchemaMarkupResponse {
  schema_type: string;
  content_length: number;
  schema_markup: any;
  generated_by: string;
  user: string;
}

export interface ContentBriefRequest {
  keyword: string;
}

export interface ContentBriefResponse {
  keyword: string;
  content_brief: {
    target_audience: string;
    content_angle: string;
    key_points: string[];
    suggested_word_count: number;
    internal_linking_opportunities: string[];
  };
  generated_by: string;
  user: string;
}

export interface AIServiceStatus {
  service_available: boolean;
  available_models: string[];
  service_provider: string;
  default_model: string;
  prompts_loaded: boolean;
  user: string;
}

class AIService {
  async generateKeywordClusters(request: KeywordClusterRequest): Promise<KeywordClusterResponse> {
    return apiClient.request<KeywordClusterResponse>({
      method: 'POST',
      url: '/ai/keyword-clusters',
      data: request,
    });
  }

  async generateSchemaMarkup(request: SchemaMarkupRequest): Promise<SchemaMarkupResponse> {
    return apiClient.request<SchemaMarkupResponse>({
      method: 'POST',
      url: '/ai/schema-markup',
      data: request,
    });
  }

  async generateContentBrief(request: ContentBriefRequest): Promise<ContentBriefResponse> {
    return apiClient.request<ContentBriefResponse>({
      method: 'POST',
      url: '/ai/content-brief',
      data: request,
    });
  }

  async getServiceStatus(): Promise<AIServiceStatus> {
    return apiClient.request<AIServiceStatus>({
      method: 'GET',
      url: '/ai/service-status',
    });
  }
}

export const aiService = new AIService();
```

### React AI Hook

```typescript
// src/hooks/useAI.ts
import { useState, useCallback } from 'react';
import { aiService, KeywordClusterRequest, SchemaMarkupRequest, ContentBriefRequest } from '../services/aiService';

export const useKeywordClusters = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [clusters, setClusters] = useState(null);
  const [error, setError] = useState<string | null>(null);

  const generateClusters = useCallback(async (request: KeywordClusterRequest) => {
    setIsGenerating(true);
    setError(null);
    
    try {
      const response = await aiService.generateKeywordClusters(request);
      setClusters(response);
      return response;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to generate keyword clusters';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsGenerating(false);
    }
  }, []);

  return {
    generateClusters,
    clusters,
    isGenerating,
    error,
  };
};

export const useSchemaMarkup = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [schema, setSchema] = useState(null);
  const [error, setError] = useState<string | null>(null);

  const generateSchema = useCallback(async (request: SchemaMarkupRequest) => {
    setIsGenerating(true);
    setError(null);
    
    try {
      const response = await aiService.generateSchemaMarkup(request);
      setSchema(response);
      return response;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to generate schema markup';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsGenerating(false);
    }
  }, []);

  return {
    generateSchema,
    schema,
    isGenerating,
    error,
  };
};

export const useContentBrief = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [brief, setBrief] = useState(null);
  const [error, setError] = useState<string | null>(null);

  const generateBrief = useCallback(async (request: ContentBriefRequest) => {
    setIsGenerating(true);
    setError(null);
    
    try {
      const response = await aiService.generateContentBrief(request);
      setBrief(response);
      return response;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to generate content brief';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsGenerating(false);
    }
  }, []);

  return {
    generateBrief,
    brief,
    isGenerating,
    error,
  };
};
```

## Error Handling

### Global Error Handler

```typescript
// src/utils/errorHandler.ts
import { AxiosError } from 'axios';

export interface APIError {
  message: string;
  status?: number;
  details?: any;
}

export const handleAPIError = (error: any): APIError => {
  if (error.response) {
    // Server responded with error status
    const { status, data } = error.response;
    
    return {
      message: data.detail || `Server error: ${status}`,
      status,
      details: data,
    };
  } else if (error.request) {
    // Request was made but no response received
    return {
      message: 'Network error: Unable to connect to server',
      status: 0,
    };
  } else {
    // Something else happened
    return {
      message: error.message || 'An unexpected error occurred',
    };
  }
};

export const getErrorMessage = (error: any): string => {
  const apiError = handleAPIError(error);
  return apiError.message;
};
```

### Error Boundary Component

```typescript
// src/components/ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="error-boundary">
            <h2>Something went wrong</h2>
            <p>{this.state.error?.message}</p>
            <button onClick={() => this.setState({ hasError: false })}>
              Try again
            </button>
          </div>
        )
      );
    }

    return this.props.children;
  }
}
```

## React Components Examples

### Site Audit Component

```typescript
// src/components/SiteAudit.tsx
import React, { useState } from 'react';
import { useAudit, useAuditStatus } from '../hooks/useAudit';

export const SiteAudit: React.FC = () => {
  const [url, setUrl] = useState('');
  const [taskId, setTaskId] = useState<string | null>(null);
  
  const { startAudit, isStarting, error: startError } = useAudit();
  const { status, isLoading, error: statusError } = useAuditStatus(taskId);

  const handleStartAudit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const task = await startAudit({ root_url: url });
      setTaskId(task.task_id);
    } catch (error) {
      console.error('Failed to start audit:', error);
    }
  };

  const renderProgress = () => {
    if (!status) return null;

    switch (status.status) {
      case 'PENDING':
        return <div>Audit is queued...</div>;
        
      case 'PROGRESS':
        const progress = status.progress;
        return (
          <div>
            <div>Phase: {progress?.phase}</div>
            <div>Progress: {progress?.progress}%</div>
            {progress?.current_url && (
              <div>Current: {progress.current_url}</div>
            )}
          </div>
        );
        
      case 'SUCCESS':
        return <div>Audit completed successfully!</div>;
        
      case 'FAILURE':
        return <div>Audit failed: {status.error}</div>;
        
      default:
        return <div>Unknown status: {status.status}</div>;
    }
  };

  return (
    <div className="site-audit">
      <h2>Site Audit</h2>
      
      <form onSubmit={handleStartAudit}>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter website URL"
          required
        />
        <button type="submit" disabled={isStarting}>
          {isStarting ? 'Starting...' : 'Start Audit'}
        </button>
      </form>

      {(startError || statusError) && (
        <div className="error">
          {startError || statusError}
        </div>
      )}

      {taskId && (
        <div className="audit-status">
          <h3>Audit Status</h3>
          {renderProgress()}
          
          {status?.status === 'SUCCESS' && status.result && (
            <div className="audit-results">
              <h4>Results</h4>
              <p>Pages crawled: {status.result.crawl_summary.total_pages_crawled}</p>
              <p>SEO issues: {status.result.seo_metrics.pages_with_missing_titles}</p>
              {/* Add more result details */}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
```

### Keyword Clusters Component

```typescript
// src/components/KeywordClusters.tsx
import React, { useState } from 'react';
import { useKeywordClusters } from '../hooks/useAI';

export const KeywordClusters: React.FC = () => {
  const [headTerm, setHeadTerm] = useState('');
  const { generateClusters, clusters, isGenerating, error } = useKeywordClusters();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      await generateClusters({ head_term: headTerm });
    } catch (error) {
      console.error('Failed to generate clusters:', error);
    }
  };

  return (
    <div className="keyword-clusters">
      <h2>Keyword Clusters</h2>
      
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={headTerm}
          onChange={(e) => setHeadTerm(e.target.value)}
          placeholder="Enter head term"
          required
        />
        <button type="submit" disabled={isGenerating}>
          {isGenerating ? 'Generating...' : 'Generate Clusters'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {clusters && (
        <div className="clusters-results">
          <h3>Keyword Clusters for "{clusters.head_term}"</h3>
          {Object.entries(clusters.clusters).map(([clusterName, keywords]) => (
            <div key={clusterName} className="cluster">
              <h4>{clusterName}</h4>
              <ul>
                {keywords.map((keyword, index) => (
                  <li key={index}>{keyword}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

This comprehensive integration guide provides all the necessary components and patterns for frontend developers to successfully integrate with the Project Aether API. The examples demonstrate proper error handling, state management, and user experience patterns for both synchronous and asynchronous operations.