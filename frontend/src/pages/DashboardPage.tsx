import { PageHeader } from "@/components/layout/PageHeader"
import { BarChart } from "@/components/charts/BarChart"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export default function DashboardPage() {
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

  return (
    <div className="container mx-auto p-6">
      <PageHeader title="Dashboard" />
      
      <div className="grid gap-6 mb-8">
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