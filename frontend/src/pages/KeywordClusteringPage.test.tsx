import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import KeywordClusteringPage from './KeywordClusteringPage'

// Mock the apiClient
vi.mock('@/lib/apiClient', () => ({
  apiClient: {
    post: vi.fn(),
  },
}))

// Mock the auth store
vi.mock('@/stores/authStore', () => ({
  useAuthStore: {
    getState: vi.fn(() => ({ token: 'mock-token' })),
  },
}))

const mockClustersResponse = {
  clusters: [
    {
      cluster_name: 'Content Strategy',
      keywords: ['content marketing strategy', 'content planning', 'content calendar'],
    },
    {
      cluster_name: 'SEO Content',
      keywords: ['seo content writing', 'content optimization', 'keyword targeting'],
    },
  ],
}

function renderWithProviders(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
      mutations: {
        retry: false,
      },
    },
  })

  return render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {ui}
      </BrowserRouter>
    </QueryClientProvider>
  )
}

describe('KeywordClusteringPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the page with initial elements', () => {
    renderWithProviders(<KeywordClusteringPage />)
    
    expect(screen.getByText('AI-Powered Keyword & Clustering Engine')).toBeInTheDocument()
    expect(screen.getByLabelText('Head Term')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Generate Clusters' })).toBeInTheDocument()
  })

  it('handles successful cluster generation', async () => {
    const user = userEvent.setup()
    const { apiClient } = await import('@/lib/apiClient')
    const mockPost = vi.mocked(apiClient.post)
    
    mockPost.mockResolvedValueOnce({
      data: mockClustersResponse,
    })

    renderWithProviders(<KeywordClusteringPage />)
    
    const headTermInput = screen.getByLabelText('Head Term')
    const generateButton = screen.getByRole('button', { name: 'Generate Clusters' })

    // Type in the head term
    await user.type(headTermInput, 'content marketing')
    expect(headTermInput).toHaveValue('content marketing')

    // Click generate button
    await user.click(generateButton)

    // Wait for results to appear
    await waitFor(() => {
      expect(screen.getByText('Keyword Clusters')).toBeInTheDocument()
    })

    // Check that cluster names are rendered
    expect(screen.getByText('Content Strategy')).toBeInTheDocument()
    expect(screen.getByText('SEO Content')).toBeInTheDocument()
    
    // Check that keyword counts are shown
    expect(screen.getByText('(3 keywords)')).toBeInTheDocument()
    
    // Check that export button appears
    expect(screen.getByRole('button', { name: 'Export to CSV' })).toBeInTheDocument()

    // Verify API was called correctly
    expect(mockPost).toHaveBeenCalledWith('/keywords/generate-clusters', {
      head_term: 'content marketing',
    })
  })

  it('disables generate button when input is empty', () => {
    renderWithProviders(<KeywordClusteringPage />)
    
    const generateButton = screen.getByRole('button', { name: 'Generate Clusters' })
    expect(generateButton).toBeDisabled()
  })

  it('handles API errors', async () => {
    const user = userEvent.setup()
    const { apiClient } = await import('@/lib/apiClient')
    const mockPost = vi.mocked(apiClient.post)
    
    mockPost.mockRejectedValueOnce(new Error('API Error'))

    renderWithProviders(<KeywordClusteringPage />)
    
    const headTermInput = screen.getByLabelText('Head Term')
    const generateButton = screen.getByRole('button', { name: 'Generate Clusters' })

    await user.type(headTermInput, 'test term')
    await user.click(generateButton)

    await waitFor(() => {
      expect(screen.getByText('Error generating clusters: API Error')).toBeInTheDocument()
    })
  })
})