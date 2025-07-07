import { useState } from "react";
import { PageHeader } from "@/components/layout/PageHeader";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { useGenerateClusters } from "@/hooks/useKeywordClusters";

export default function KeywordClusteringPage() {
  const [headTerm, setHeadTerm] = useState("");
  const generateClusters = useGenerateClusters();

  const handleGenerate = async () => {
    if (!headTerm.trim()) return;
    
    generateClusters.mutate(headTerm);
  };

  const handleExportCSV = () => {
    if (!generateClusters.data?.clusters) return;
    
    const csvContent = generateClusters.data.clusters.map(cluster => 
      cluster.keywords.map(keyword => `${cluster.cluster_name},${keyword}`).join('\n')
    ).join('\n');
    
    const blob = new Blob([`Cluster,Keyword\n${csvContent}`], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `keyword-clusters-${headTerm}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="container mx-auto p-8 space-y-8 animate-slide-up">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold gradient-text font-inter tracking-tight">
          AI-Powered Keyword & Clustering Engine
        </h1>
        <p className="text-lg text-text-secondary font-inter max-w-2xl mx-auto">
          Enter a head term to generate semantically related keyword clusters using advanced AI
        </p>
      </div>
      
      <section className="max-w-2xl mx-auto">
        <div className="glassmorphism p-8 space-y-6">
          <div className="space-y-3">
            <Label htmlFor="head-term">Enter Keywords</Label>
            <Input
              id="head-term"
              value={headTerm}
              onChange={(e) => setHeadTerm(e.target.value)}
              placeholder="Enter keywords separated by commas or new lines"
              className="w-full"
            />
            <p className="text-sm text-text-secondary font-inter">
              Separate multiple keywords with commas or new lines
            </p>
          </div>
          <Button 
            onClick={handleGenerate}
            disabled={!headTerm.trim() || generateClusters.isPending}
            className="w-full"
            size="lg"
          >
            {generateClusters.isPending ? "🔄 Generating..." : "✨ Generate Clusters"}
          </Button>
        </div>
      </section>

      {generateClusters.isError && (
        <section className="max-w-2xl mx-auto">
          <div className="glassmorphism p-6 border-red-200 bg-red-50/70">
            <h3 className="text-lg font-semibold text-red-700 mb-2 font-inter">Error</h3>
            <p className="text-red-600 font-inter">
              Error generating clusters: {generateClusters.error?.message}
            </p>
          </div>
        </section>
      )}

      {generateClusters.data?.clusters && generateClusters.data.clusters.length > 0 && (
        <section className="max-w-4xl mx-auto space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-3xl font-bold text-text-primary font-inter">Keyword Clusters</h2>
            <Button onClick={handleExportCSV} variant="outline" size="lg">
              📊 Export to CSV
            </Button>
          </div>
          
          <div className="grid gap-6">
            {generateClusters.data.clusters.map((cluster, index) => (
              <div key={index} className="glassmorphism p-6 hover-lift animate-fade-in" style={{ animationDelay: `${index * 100}ms` }}>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-text-primary font-inter">{cluster.cluster_name}</h3>
                  <span className="bg-accent text-white px-3 py-1 rounded-full text-sm font-medium">
                    {cluster.keywords.length} keywords
                  </span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {cluster.keywords.map((keyword, keywordIndex) => (
                    <span 
                      key={keywordIndex} 
                      className="bg-secondary-action text-text-primary px-3 py-1 rounded-lg text-sm font-medium border border-secondary-border hover:shadow-soft transition-all duration-200"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}