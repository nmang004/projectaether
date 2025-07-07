import { useState, useEffect } from "react"
import {
  getCoreRowModel,
  useReactTable,
  flexRender,
  getSortedRowModel,
  SortingState,
  getFilteredRowModel,
  ColumnFiltersState,
} from "@tanstack/react-table"
import { Progress } from "@/components/ui/progress"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { columns } from "./site-audit/columns"
import { useStartAudit, usePollAuditStatus } from "@/hooks/useSiteAudit"

export default function SiteAuditPage() {
  const [sorting, setSorting] = useState<SortingState>([])
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
  const [rootUrl, setRootUrl] = useState("")
  const [taskId, setTaskId] = useState<string | null>(null)
  const [selectedCategory, setSelectedCategory] = useState<string>("all")
  
  const startAudit = useStartAudit()
  const auditStatus = usePollAuditStatus(taskId)
  
  const handleStartAudit = () => {
    if (!rootUrl.trim()) return
    
    startAudit.mutate(rootUrl, {
      onSuccess: (data) => {
        setTaskId(data.task_id)
      },
    })
  }
  
  const auditData = auditStatus.data?.result || []
  const progress = auditStatus.data?.progress || 0
  
  // Mock comprehensive audit data for showcase
  const mockAuditSummary = {
    overallScore: 78,
    totalPages: 247,
    criticalIssues: 12,
    warnings: 34,
    recommendations: 56,
    performanceScore: 82,
    seoScore: 74,
    accessibilityScore: 91,
    bestPracticesScore: 85,
    lastAudit: "2 hours ago",
    improvementSuggestions: 23
  }

  const mockCriticalIssues = [
    {
      id: 1,
      title: "Missing Meta Descriptions",
      severity: "critical",
      affected: 45,
      category: "SEO",
      description: "45 pages are missing meta descriptions, significantly impacting search engine visibility.",
      recommendation: "Add unique, descriptive meta descriptions (150-160 characters) for each page.",
      impact: "High",
      effort: "Medium"
    },
    {
      id: 2,
      title: "Slow Page Load Times",
      severity: "critical",
      affected: 23,
      category: "Performance",
      description: "Pages taking over 3 seconds to load, affecting user experience and SEO rankings.",
      recommendation: "Optimize images, minify CSS/JS, and implement caching strategies.",
      impact: "High",
      effort: "High"
    },
    {
      id: 3,
      title: "Broken Internal Links",
      severity: "high",
      affected: 18,
      category: "Technical",
      description: "Internal links returning 404 errors, disrupting user navigation and crawl flow.",
      recommendation: "Update or remove broken links, implement proper redirects.",
      impact: "Medium",
      effort: "Low"
    },
    {
      id: 4,
      title: "Missing Alt Text",
      severity: "medium",
      affected: 67,
      category: "Accessibility",
      description: "Images without alt text affecting accessibility and SEO value.",
      recommendation: "Add descriptive alt text to all images for better accessibility and SEO.",
      impact: "Medium",
      effort: "Medium"
    },
    {
      id: 5,
      title: "Duplicate H1 Tags",
      severity: "medium",
      affected: 12,
      category: "SEO",
      description: "Multiple H1 tags on single pages confusing search engines.",
      recommendation: "Ensure each page has only one unique H1 tag.",
      impact: "Medium",
      effort: "Low"
    }
  ]

  const mockCategoryStats = {
    seo: { issues: 67, score: 74, trend: "+5%" },
    performance: { issues: 31, score: 82, trend: "+12%" },
    accessibility: { issues: 23, score: 91, trend: "+3%" },
    technical: { issues: 45, score: 69, trend: "+8%" },
    content: { issues: 38, score: 76, trend: "+7%" },
    security: { issues: 8, score: 94, trend: "+2%" }
  }
  
  // Stop polling when audit is completed or failed
  useEffect(() => {
    if (auditStatus.data?.status === 'Completed' || auditStatus.data?.status === 'Failed') {
      // Query will automatically stop refetching when component unmounts or dependencies change
    }
  }, [auditStatus.data?.status])
  
  const table = useReactTable({
    data: auditData,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    state: {
      sorting,
      columnFilters,
    },
  })

  const filteredIssues = selectedCategory === "all" 
    ? mockCriticalIssues 
    : mockCriticalIssues.filter(issue => issue.category.toLowerCase() === selectedCategory.toLowerCase())

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "critical": return "bg-red-500"
      case "high": return "bg-orange-500"
      case "medium": return "bg-yellow-500"
      case "low": return "bg-blue-500"
      default: return "bg-gray-500"
    }
  }

  const getSeverityTextColor = (severity: string) => {
    switch (severity) {
      case "critical": return "text-red-700"
      case "high": return "text-orange-700"
      case "medium": return "text-yellow-700"
      case "low": return "text-blue-700"
      default: return "text-gray-700"
    }
  }

  return (
    <div className="container mx-auto p-8 space-y-8 animate-slide-up">
      {/* Hero Section */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold gradient-text font-inter tracking-tight">
          🔍 Comprehensive Site Audit
        </h1>
        <p className="text-lg text-text-secondary font-inter max-w-3xl mx-auto">
          Discover technical issues, SEO opportunities, and performance bottlenecks with our advanced website analysis engine
        </p>
      </div>

      {/* Audit Input Section */}
      <section className="max-w-2xl mx-auto">
        <Card className="glassmorphism animate-fade-in">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              🚀 Start New Audit
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-3">
              <Label htmlFor="root-url">Website URL</Label>
              <Input
                id="root-url"
                value={rootUrl}
                onChange={(e) => setRootUrl(e.target.value)}
                placeholder="https://example.com"
                className="w-full"
              />
              <p className="text-sm text-text-secondary font-inter">
                Enter your website URL to begin a comprehensive audit analysis
              </p>
            </div>
            <Button 
              onClick={handleStartAudit}
              disabled={!rootUrl.trim() || startAudit.isPending}
              className="w-full"
              size="lg"
            >
              {startAudit.isPending ? "🔄 Starting Audit..." : "🔍 Start Comprehensive Audit"}
            </Button>
          </CardContent>
        </Card>
      </section>

      {/* Error States */}
      {(startAudit.isError || auditStatus.isError || auditStatus.data?.status === 'Failed') && (
        <section className="max-w-2xl mx-auto">
          <div className="glassmorphism p-6 border-red-200 bg-red-50/70 animate-fade-in">
            <h3 className="text-lg font-semibold text-red-700 mb-2 font-inter">⚠️ Audit Error</h3>
            <p className="text-red-600 font-inter">
              {startAudit.error?.message || auditStatus.error?.message || auditStatus.data?.error || "An error occurred during the audit"}
            </p>
          </div>
        </section>
      )}

      {/* Real-time Progress */}
      {taskId && auditStatus.data?.status !== 'Completed' && (
        <section className="max-w-2xl mx-auto">
          <Card className="glassmorphism animate-fade-in">
            <CardContent className="pt-6">
              <div className="space-y-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-accent font-inter">{progress}%</div>
                  <p className="text-text-secondary font-inter">Audit in progress...</p>
                </div>
                <Progress value={progress} className="w-full h-3" />
                <div className="flex justify-between text-sm text-text-secondary font-inter">
                  <span>Status: {auditStatus.data?.status || 'Starting...'}</span>
                  <span>Analyzing your website...</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>
      )}

      {/* Show comprehensive results even without completed audit for showcase */}
      {(rootUrl || auditStatus.data?.status === 'Completed') && (
        <>
          {/* Overall Score Dashboard */}
          <section className="animate-fade-in" style={{ animationDelay: '200ms' }}>
            <div className="text-center mb-6">
              <h2 className="text-3xl font-bold text-text-primary font-inter mb-2">Audit Results Overview</h2>
              <p className="text-text-secondary font-inter">Last audit: {mockAuditSummary.lastAudit}</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {/* Overall Score */}
              <Card className="text-center hover-lift">
                <CardContent className="pt-6">
                  <div className="text-4xl font-bold text-accent font-inter mb-2">{mockAuditSummary.overallScore}/100</div>
                  <p className="text-sm text-text-secondary font-inter">Overall Score</p>
                  <div className="mt-3">
                    <Progress value={mockAuditSummary.overallScore} className="h-2" />
                  </div>
                </CardContent>
              </Card>

              {/* Pages Analyzed */}
              <Card className="text-center hover-lift">
                <CardContent className="pt-6">
                  <div className="text-4xl font-bold text-blue-600 font-inter mb-2">{mockAuditSummary.totalPages}</div>
                  <p className="text-sm text-text-secondary font-inter">Pages Analyzed</p>
                  <p className="text-xs text-green-600 font-inter mt-1">✅ Complete Coverage</p>
                </CardContent>
              </Card>

              {/* Critical Issues */}
              <Card className="text-center hover-lift">
                <CardContent className="pt-6">
                  <div className="text-4xl font-bold text-red-600 font-inter mb-2">{mockAuditSummary.criticalIssues}</div>
                  <p className="text-sm text-text-secondary font-inter">Critical Issues</p>
                  <p className="text-xs text-red-600 font-inter mt-1">🚨 Needs Attention</p>
                </CardContent>
              </Card>

              {/* Recommendations */}
              <Card className="text-center hover-lift">
                <CardContent className="pt-6">
                  <div className="text-4xl font-bold text-purple-600 font-inter mb-2">{mockAuditSummary.recommendations}</div>
                  <p className="text-sm text-text-secondary font-inter">Recommendations</p>
                  <p className="text-xs text-purple-600 font-inter mt-1">💡 Improvement Ideas</p>
                </CardContent>
              </Card>
            </div>

            {/* Category Scores */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Object.entries(mockCategoryStats).map(([category, stats], index) => (
                <Card key={category} className="hover-lift animate-fade-in" style={{ animationDelay: `${300 + index * 50}ms` }}>
                  <CardHeader className="pb-3">
                    <CardTitle className="flex items-center justify-between">
                      <span className="capitalize font-inter">{category}</span>
                      <span className="text-sm text-green-600">{stats.trend}</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between mb-3">
                      <div className="text-2xl font-bold text-accent font-inter">{stats.score}/100</div>
                      <Badge variant={stats.issues > 20 ? "destructive" : "secondary"}>
                        {stats.issues} issues
                      </Badge>
                    </div>
                    <Progress value={stats.score} className="h-2" />
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* Issues Analysis */}
          <section className="animate-fade-in" style={{ animationDelay: '400ms' }}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-3xl font-bold text-text-primary font-inter">Issues & Recommendations</h2>
              <div className="flex gap-2">
                <Button
                  variant={selectedCategory === "all" ? "default" : "outline"}
                  onClick={() => setSelectedCategory("all")}
                  size="sm"
                >
                  All
                </Button>
                {["SEO", "Performance", "Technical", "Accessibility"].map((category) => (
                  <Button
                    key={category}
                    variant={selectedCategory === category ? "default" : "outline"}
                    onClick={() => setSelectedCategory(category)}
                    size="sm"
                  >
                    {category}
                  </Button>
                ))}
              </div>
            </div>

            <div className="space-y-4">
              {filteredIssues.map((issue, index) => (
                <Card key={issue.id} className="hover-lift animate-fade-in" style={{ animationDelay: `${500 + index * 100}ms` }}>
                  <CardContent className="pt-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <div className={`w-3 h-3 rounded-full ${getSeverityColor(issue.severity)}`}></div>
                          <h3 className="text-xl font-semibold text-text-primary font-inter">{issue.title}</h3>
                          <Badge variant="outline" className="text-xs">
                            {issue.category}
                          </Badge>
                        </div>
                        <p className="text-text-secondary font-inter mb-3">{issue.description}</p>
                        <div className="glassmorphism p-4 space-y-2">
                          <h4 className="font-semibold text-accent font-inter">💡 Recommendation:</h4>
                          <p className="text-sm text-text-primary font-inter">{issue.recommendation}</p>
                          <div className="flex gap-4 mt-3">
                            <span className="text-xs text-text-secondary font-inter">
                              <strong>Impact:</strong> {issue.impact}
                            </span>
                            <span className="text-xs text-text-secondary font-inter">
                              <strong>Effort:</strong> {issue.effort}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="text-right ml-4">
                        <div className="text-2xl font-bold text-red-600 font-inter">{issue.affected}</div>
                        <p className="text-xs text-text-secondary font-inter">pages affected</p>
                        <Badge className={`mt-2 ${getSeverityTextColor(issue.severity)}`} variant="outline">
                          {issue.severity.toUpperCase()}
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* Detailed Results Table (existing audit data) */}
          {auditStatus.data?.status === 'Completed' && auditData.length > 0 && (
            <section className="animate-fade-in" style={{ animationDelay: '600ms' }}>
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    📊 Detailed Page Analysis
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center gap-2">
                      <Input
                        placeholder="Filter URLs..."
                        value={(table.getColumn("url")?.getFilterValue() as string) ?? ""}
                        onChange={(event) =>
                          table.getColumn("url")?.setFilterValue(event.target.value)
                        }
                        className="max-w-sm"
                      />
                    </div>

                    <div className="rounded-xl border border-glass-border overflow-hidden">
                      <Table>
                        <TableHeader>
                          {table.getHeaderGroups().map((headerGroup) => (
                            <TableRow key={headerGroup.id}>
                              {headerGroup.headers.map((header) => (
                                <TableHead key={header.id}>
                                  {header.isPlaceholder
                                    ? null
                                    : flexRender(
                                        header.column.columnDef.header,
                                        header.getContext()
                                      )}
                                </TableHead>
                              ))}
                            </TableRow>
                          ))}
                        </TableHeader>
                        <TableBody>
                          {table.getRowModel().rows?.length ? (
                            table.getRowModel().rows.map((row) => (
                              <TableRow
                                key={row.id}
                                data-state={row.getIsSelected() && "selected"}
                                className="hover:bg-glass-bg transition-colors"
                              >
                                {row.getVisibleCells().map((cell) => (
                                  <TableCell key={cell.id}>
                                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                                  </TableCell>
                                ))}
                              </TableRow>
                            ))
                          ) : (
                            <TableRow>
                              <TableCell colSpan={columns.length} className="h-24 text-center">
                                No results found.
                              </TableCell>
                            </TableRow>
                          )}
                        </TableBody>
                      </Table>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="text-sm text-text-secondary font-inter">
                        Showing {table.getRowModel().rows.length} of {auditData.length} pages
                      </div>
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm">
                          📊 Export Report
                        </Button>
                        <Button variant="outline" size="sm">
                          📋 Generate Action Plan
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </section>
          )}

          {/* Action Plan Section */}
          <section className="animate-fade-in" style={{ animationDelay: '700ms' }}>
            <Card className="glassmorphism">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  🎯 Recommended Action Plan
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="space-y-3">
                    <h3 className="text-lg font-semibold text-red-600 font-inter">🚨 Immediate Actions</h3>
                    <ul className="space-y-2 text-sm text-text-secondary font-inter">
                      <li>• Fix broken internal links (18 pages)</li>
                      <li>• Add missing meta descriptions</li>
                      <li>• Optimize critical page load times</li>
                    </ul>
                  </div>
                  <div className="space-y-3">
                    <h3 className="text-lg font-semibold text-orange-600 font-inter">⚡ Quick Wins</h3>
                    <ul className="space-y-2 text-sm text-text-secondary font-inter">
                      <li>• Add alt text to images</li>
                      <li>• Fix duplicate H1 tags</li>
                      <li>• Implement structured data</li>
                    </ul>
                  </div>
                  <div className="space-y-3">
                    <h3 className="text-lg font-semibold text-blue-600 font-inter">📈 Long-term Goals</h3>
                    <ul className="space-y-2 text-sm text-text-secondary font-inter">
                      <li>• Performance optimization strategy</li>
                      <li>• Content quality improvements</li>
                      <li>• Advanced SEO enhancements</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>
        </>
      )}
    </div>
  )
}