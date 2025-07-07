import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { apiClient } from '@/lib/apiClient'

function HomePage() {
  const { data: apiHealth, isLoading } = useQuery({
    queryKey: ['api-health'],
    queryFn: () => apiClient.get('/health'),
  })

  return (
    <div className="container mx-auto py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold tracking-tight">Project Aether</h1>
        <p className="text-lg text-muted-foreground mt-2">
          Unified SEO Intelligence Platform
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              API Status 
              {isLoading ? (
                <Badge variant="secondary">Checking...</Badge>
              ) : apiHealth?.data?.status === 'healthy' ? (
                <Badge variant="default">Healthy</Badge>
              ) : (
                <Badge variant="destructive">Offline</Badge>
              )}
            </CardTitle>
            <CardDescription>
              Backend API connection status
            </CardDescription>
          </CardHeader>
          <CardContent>
            {apiHealth && (
              <div className="space-y-2 text-sm">
                <p><strong>Service:</strong> {apiHealth.data.service}</p>
                <p><strong>Version:</strong> {apiHealth.data.version}</p>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Site Audits</CardTitle>
            <CardDescription>
              Technical SEO crawler and analysis
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Coming soon - comprehensive site crawling and technical SEO analysis.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Content Briefs</CardTitle>
            <CardDescription>
              AI-powered content strategy
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Coming soon - SERP-driven content brief generation.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Keyword Research</CardTitle>
            <CardDescription>
              AI clustering and analysis
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Coming soon - semantic keyword clustering and intent analysis.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Schema Generator</CardTitle>
            <CardDescription>
              Automated structured data
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Coming soon - AI-powered JSON-LD schema markup generation.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Internal Linking</CardTitle>
            <CardDescription>
              Smart link opportunities
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Coming soon - AI-assisted internal linking analysis.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default HomePage