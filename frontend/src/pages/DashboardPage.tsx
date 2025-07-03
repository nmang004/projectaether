import { useState } from 'react';
import { PageHeader } from "@/components/layout/PageHeader"
import { BarChart } from "@/components/charts/BarChart"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { useAuthStore } from '@/stores/authStore';

export default function DashboardPage() {
  const [keywords, setKeywords] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [clusters, setClusters] = useState([]);
  const { logout } = useAuthStore();

  const performanceData = [
    { name: 'Organic Traffic', value: 12500 },
    { name: 'Keyword Rankings', value: 892 },
    { name: 'Backlinks', value: 2340 },
    { name: 'Pages Indexed', value: 1150 },
  ]

  const competitorData = [
    { name: 'Ahrefs', value: 89 },
    { name: 'Semrush', value: 92 },
    { name: 'Moz', value: 76 },
    { name: 'Your Site', value: 85 },
  ]

  const recentAudits = [
    { site: 'example.com', score: 87, issues: 12, status: 'completed' },
    { site: 'demo.com', score: 72, issues: 24, status: 'in_progress' },
    { site: 'test.com', score: 91, issues: 8, status: 'completed' },
  ]

  const handleGenerateClusters = async () => {
    setIsLoading(true);
    // Mock cluster generation
    setTimeout(() => {
      setClusters([
        {
          id: 1,
          primaryKeyword: 'SEO tools',
          relatedKeywords: ['keyword research', 'SERP analysis', 'backlink checker']
        },
        {
          id: 2,
          primaryKeyword: 'content marketing',
          relatedKeywords: ['blog writing', 'social media', 'email marketing']
        }
      ]);
      setIsLoading(false);
    }, 2000);
  };

  return (
    <div className="container mx-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold" data-testid="welcome-header">Welcome to Project Aether</h1>
        <Button onClick={logout} variant="outline" data-testid="logout-button">
          Logout
        </Button>
      </div>
      
      <div className="grid gap-6 mb-8">
        <Card>
          <CardHeader>
            <CardTitle>Keyword Clustering</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="keywords" className="text-sm font-medium">Enter Keywords</label>
              <Textarea
                id="keywords"
                placeholder="Enter keywords separated by commas or new lines"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                rows={4}
                data-testid="keyword-textarea"
              />
            </div>
            <Button 
              onClick={handleGenerateClusters} 
              disabled={!keywords.trim() || isLoading}
              data-testid="generate-clusters-button"
            >
              {isLoading ? 'Generating...' : 'Generate Clusters'}
            </Button>
            {isLoading && (
              <div className="flex items-center space-x-2" data-testid="loading-indicator">
                <div className="animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full"></div>
                <span>Generating keyword clusters...</span>
              </div>
            )}
            {clusters.length > 0 && (
              <div className="space-y-4" data-testid="results-container">
                <h3 className="text-lg font-medium">Generated Clusters</h3>
                {clusters.map((cluster) => (
                  <div key={cluster.id} className="border rounded-lg p-4" data-testid="cluster-group">
                    <h4 className="font-medium text-blue-600" data-testid="primary-keyword">
                      {cluster.primaryKeyword}
                    </h4>
                    <div className="mt-2" data-testid="related-keyword-list">
                      <span className="text-sm text-gray-600">Related keywords: </span>
                      {cluster.relatedKeywords.map((keyword, index) => (
                        <span key={index} className="text-sm" data-testid="related-keyword-item">
                          {keyword}{index < cluster.relatedKeywords.length - 1 ? ', ' : ''}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>SEO Performance Overview</CardTitle>
            </CardHeader>
            <CardContent>
              <BarChart 
                data={performanceData} 
                height={300}
                barColor="#10b981"
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Competitor Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <BarChart 
                data={competitorData} 
                height={300}
                barColor="#8b5cf6"
              />
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Recent Site Audits</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentAudits.map((audit, index) => (
                <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div>
                      <h3 className="font-medium">{audit.site}</h3>
                      <div className="flex items-center space-x-2 mt-1">
                        <span className="text-sm text-muted-foreground">Score: {audit.score}</span>
                        <span className="text-sm text-muted-foreground">•</span>
                        <span className="text-sm text-muted-foreground">{audit.issues} issues</span>
                      </div>
                    </div>
                  </div>
                  <Badge variant={audit.status === 'completed' ? 'default' : 'secondary'}>
                    {audit.status === 'completed' ? 'Complete' : 'In Progress'}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}