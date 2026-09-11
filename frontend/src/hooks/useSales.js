import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { createSale, getSalesAnalytics, importSales, listSales } from '@satgit/api-client'

export function useSales(filters = {}) {
  return useQuery({
    queryKey: ['sales', filters],
    queryFn: () => listSales(filters),
  })
}

export function useCreateSale() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: createSale,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['sales'] }),
  })
}

export function useSalesAnalytics(groupBy = 'week') {
  return useQuery({
    queryKey: ['sales-analytics', groupBy],
    queryFn: () => getSalesAnalytics(groupBy),
  })
}

export function useImportSales() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: importSales,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sales'] })
      queryClient.invalidateQueries({ queryKey: ['sales-analytics'] })
    },
  })
}
