import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { askAgent, askAgentDeep, getAgentHistory } from '@satgit/api-client'

export function useAgentHistory(limit = 20) {
  return useQuery({ queryKey: ['agent-history', limit], queryFn: () => getAgentHistory(limit) })
}

export function useAskAgent() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: askAgent,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['agent-history'] }),
  })
}

export function useAskAgentDeep() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: askAgentDeep,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['agent-history'] }),
  })
}
