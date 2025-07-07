import { useState } from 'react';
import { BarChart } from "@/components/charts/BarChart"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { useAuthStore } from '@/stores/authStore';

export default function DashboardPage() {
  const [keywords, setKeywords] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [clusters, setClusters] = useState<Array<{id: number; primaryKeyword: string; relatedKeywords: string[]}>>([]);
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
    <div className="container mx-auto p-8 space-y-8 animate-slide-up">
      {/* Hero Section */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold gradient-text font-inter tracking-tight" data-testid="welcome-header">
          Welcome to Project Aether
        </h1>
        <p className="text-lg text-text-secondary font-inter max-w-2xl mx-auto">
          Your comprehensive SEO intelligence platform for advanced keyword research, site auditing, and competitor analysis
        </p>
      </div>
      
      {/* Bento Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 xl:grid-cols-4 gap-6 auto-rows-fr">
        
        {/* Keyword Clustering - Large Card */}
        <Card className="lg:col-span-2 xl:col-span-2 min-h-[400px] animate-fade-in">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              ✨ Keyword Clustering
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <label htmlFor="keywords" className="text-sm font-medium font-inter text-text-secondary block">Enter Keywords</label>
              <Textarea
                id="keywords"
                placeholder="Enter keywords separated by commas or new lines"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                rows={4}
                data-testid="keyword-textarea"
                className="rounded-xl border-secondary-border focus:ring-accent"
              />
            </div>
            <Button 
              onClick={handleGenerateClusters} 
              disabled={!keywords.trim() || isLoading}
              data-testid="generate-clusters-button"
              className="w-full"
              size="lg"
            >
              {isLoading ? '🔄 Generating...' : '🚀 Generate Clusters'}
            </Button>
            {isLoading && (
              <div className="flex items-center justify-center space-x-2 p-4 glassmorphism" data-testid="loading-indicator">
                <div className="animate-spin h-5 w-5 border-2 border-accent border-t-transparent rounded-full"></div>
                <span className="font-inter text-text-secondary">Generating keyword clusters...</span>
              </div>
            )}
            {clusters.length > 0 && (
              <div className="space-y-3" data-testid="results-container">
                <h3 className="text-lg font-semibold font-inter text-text-primary">Generated Clusters</h3>
                {clusters.map((cluster) => (
                  <div key={cluster.id} className="glassmorphism p-4 space-y-2" data-testid="cluster-group">
                    <h4 className="font-semibold text-accent font-inter" data-testid="primary-keyword">
                      {cluster.primaryKeyword}
                    </h4>
                    <div className="flex flex-wrap gap-1" data-testid="related-keyword-list">
                      {cluster.relatedKeywords.map((keyword, index) => (
                        <span key={index} className="bg-secondary-action text-text-primary px-2 py-1 rounded-md text-xs font-medium border border-secondary-border" data-testid="related-keyword-item">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Performance Overview */}
        <Card className="lg:col-span-1 xl:col-span-2 min-h-[400px] animate-fade-in" style={{ animationDelay: '100ms' }}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              📊 SEO Performance Overview
            </CardTitle>
          </CardHeader>
          <CardContent>
            <BarChart 
              data={performanceData} 
              height={300}
              barColor="#10b981"
            />
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <div className="lg:col-span-3 xl:col-span-4 grid grid-cols-2 lg:grid-cols-4 gap-4">
          {performanceData.map((stat, index) => (
            <Card key={stat.name} className="p-4 text-center hover-lift animate-fade-in" style={{ animationDelay: `${200 + index * 50}ms` }}>
              <div className="text-2xl font-bold text-accent font-inter">{stat.value.toLocaleString()}</div>
              <div className="text-sm text-text-secondary font-inter">{stat.name}</div>
            </Card>
          ))}
        </div>

        {/* Competitor Analysis */}
        <Card className="lg:col-span-2 xl:col-span-2 min-h-[350px] animate-fade-in" style={{ animationDelay: '150ms' }}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              🏆 Competitor Analysis
            </CardTitle>
          </CardHeader>
          <CardContent>
            <BarChart 
              data={competitorData} 
              height={250}
              barColor="#8b5cf6"
            />
          </CardContent>
        </Card>

        {/* Recent Audits */}
        <Card className="lg:col-span-1 xl:col-span-2 min-h-[350px] animate-fade-in" style={{ animationDelay: '200ms' }}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              🔍 Recent Site Audits
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {recentAudits.map((audit, index) => (
                <div key={index} className="glassmorphism p-4 hover-lift transition-all duration-200">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-semibold font-inter text-text-primary">{audit.site}</h3>
                      <div className="flex items-center space-x-2 mt-1">
                        <span className="text-sm text-text-secondary font-inter">Score: {audit.score}</span>
                        <span className="text-sm text-text-secondary">•</span>
                        <span className="text-sm text-text-secondary font-inter">{audit.issues} issues</span>
                      </div>
                    </div>
                    <Badge variant={audit.status === 'completed' ? 'default' : 'secondary'} className="rounded-full">
                      {audit.status === 'completed' ? '✅ Complete' : '⏳ In Progress'}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}