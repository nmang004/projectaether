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
    <div className="container mx-auto p-6">
      <PageHeader title="AI-Powered Keyword & Clustering Engine" />
      
      <section className="mb-8">
        <div className="max-w-md space-y-4">
          <div className="space-y-2">
            <Label htmlFor="head-term">Head Term</Label>
            <Input
              id="head-term"
              value={headTerm}
              onChange={(e) => setHeadTerm(e.target.value)}
              placeholder="e.g., content marketing"
              className="w-full"
            />
          </div>
          <Button 
            onClick={handleGenerate}
            disabled={!headTerm.trim() || generateClusters.isPending}
            className="w-full"
          >
            {generateClusters.isPending ? "Generating..." : "Generate Clusters"}
          </Button>
        </div>
      </section>

      {generateClusters.isError && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-700">
            Error generating clusters: {generateClusters.error?.message}
          </p>
        </div>
      )}

      {generateClusters.data?.clusters && generateClusters.data.clusters.length > 0 && (
        <section>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Keyword Clusters</h2>
            <Button onClick={handleExportCSV} variant="outline">
              Export to CSV
            </Button>
          </div>
          
          <Accordion type="single" collapsible className="w-full">
            {generateClusters.data.clusters.map((cluster, index) => (
              <AccordionItem key={index} value={index.toString()}>
                <AccordionTrigger className="text-left">
                  <span className="font-medium">{cluster.cluster_name}</span>
                  <span className="text-sm text-muted-foreground ml-2">
                    ({cluster.keywords.length} keywords)
                  </span>
                </AccordionTrigger>
                <AccordionContent>
                  <ul className="space-y-1 pl-4">
                    {cluster.keywords.map((keyword, keywordIndex) => (
                      <li key={keywordIndex} className="text-sm">
                        • {keyword}
                      </li>
                    ))}
                  </ul>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </section>
      )}
    </div>
  );
}