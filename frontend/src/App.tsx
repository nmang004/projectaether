import { Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from './components/ui/toaster';
import { AppLayout } from './components/layout/AppLayout';
import ProtectedRoute from './components/auth/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import { useAuthStore } from './stores/authStore';

// Lazy load components to prevent loading errors
import { Suspense, lazy } from 'react';

const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const SiteAuditPage = lazy(() => import('./pages/SiteAuditPage'));
const KeywordClusteringPage = lazy(() => import('./pages/KeywordClusteringPage'));

// Loading component
const LoadingPage = () => (
  <div style={{ 
    display: 'flex', 
    justifyContent: 'center', 
    alignItems: 'center', 
    height: '100vh',
    fontFamily: 'Arial, sans-serif'
  }}>
    <div>
      <h2>🚀 Loading...</h2>
      <p>Please wait while we load the application.</p>
    </div>
  </div>
);

// Error fallback component
const ErrorFallback = ({ error }: { error: Error }) => (
  <div style={{ 
    padding: '20px', 
    textAlign: 'center', 
    fontFamily: 'Arial, sans-serif',
    color: 'red'
  }}>
    <h2>❌ Component Loading Error</h2>
    <details>
      <summary>Error Details</summary>
      <pre style={{ textAlign: 'left', background: '#f5f5f5', padding: '10px' }}>
        {error.toString()}
      </pre>
    </details>
  </div>
);

function App() {
  const { token } = useAuthStore();
  
  console.log('🔧 App component rendering, token exists:', !!token);
  
  try {
    return (
      <>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route 
            path="/*" 
            element={
              <ProtectedRoute>
                <AppLayout>
                  <Suspense fallback={<LoadingPage />}>
                    <Routes>
                      <Route index element={<DashboardPage />} />
                      <Route path="site-audit" element={<SiteAuditPage />} />
                      <Route path="keyword-clustering" element={<KeywordClusteringPage />} />
                      <Route path="*" element={<Navigate to="/" replace />} />
                    </Routes>
                  </Suspense>
                </AppLayout>
              </ProtectedRoute>
            } 
          />
        </Routes>
        <Toaster />
      </>
    );
  } catch (error) {
    console.error('❌ Error in App component:', error);
    return <ErrorFallback error={error as Error} />;
  }
}

export default App