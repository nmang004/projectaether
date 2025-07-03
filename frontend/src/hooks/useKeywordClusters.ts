import { useMutation } from '@tanstack/react-query';
import { apiClient } from '@/lib/apiClient';

interface KeywordCluster {
  cluster_name: string;
  keywords: string[];
}

interface GenerateClustersResponse {
  clusters: KeywordCluster[];
}

interface GenerateClustersRequest {
  head_term: string;
}

export const useGenerateClusters = () => {
  return useMutation<GenerateClustersResponse, Error, string>({
    mutationFn: async (headTerm: string) => {
      const response = await apiClient.post<GenerateClustersResponse>(
        '/keywords/generate-clusters',
        { head_term: headTerm } as GenerateClustersRequest
      );
      return response.data;
    },
  });
};