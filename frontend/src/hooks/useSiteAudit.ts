import { useMutation, useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/apiClient';

interface StartAuditRequest {
  root_url: string;
}

interface StartAuditResponse {
  task_id: string;
}

interface AuditResult {
  url: string;
  status_code: number;
  response_time: number;
  page_title: string;
  meta_description: string;
  h1_tags: string[];
  issues: string[];
}

interface AuditStatusResponse {
  status: 'In Progress' | 'Completed' | 'Failed';
  progress: number;
  result: AuditResult[] | null;
  error?: string;
}

export const useStartAudit = () => {
  return useMutation<StartAuditResponse, Error, string>({
    mutationFn: async (rootUrl: string) => {
      const response = await apiClient.post<StartAuditResponse>(
        '/audits/start',
        { root_url: rootUrl } as StartAuditRequest
      );
      return response.data;
    },
  });
};

export const usePollAuditStatus = (taskId: string | null) => {
  return useQuery<AuditStatusResponse, Error>({
    queryKey: ['auditStatus', taskId],
    queryFn: async () => {
      if (!taskId) throw new Error('Task ID is required');
      const response = await apiClient.get<AuditStatusResponse>(`/audits/status/${taskId}`);
      return response.data;
    },
    enabled: !!taskId,
    refetchInterval: 5000, // Poll every 5 seconds
    refetchIntervalInBackground: false,
  });
};