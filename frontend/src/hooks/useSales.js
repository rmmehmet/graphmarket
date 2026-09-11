import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { createSale, listSales } from '../services/salesService'

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
