import { useQuery } from '@tanstack/react-query'
import { getUsage } from '../services/usageService'

export function useUsage() {
  return useQuery({ queryKey: ['usage'], queryFn: getUsage })
}
