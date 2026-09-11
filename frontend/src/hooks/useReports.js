import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { generateReport, getReport, listReports } from '@satgit/api-client'

export function useReports() {
  return useQuery({ queryKey: ['reports'], queryFn: listReports })
}

export function useReport(reportId) {
  return useQuery({
    queryKey: ['report', reportId],
    queryFn: () => getReport(reportId),
    enabled: Boolean(reportId),
  })
}

export function useGenerateReport() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: generateReport,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['reports'] }),
  })
}
