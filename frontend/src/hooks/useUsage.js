import { useQuery } from '@tanstack/react-query'
import { getUsage } from '@satgit/api-client'

export function useUsage() {
  return useQuery({ queryKey: ['usage'], queryFn: getUsage })
}
