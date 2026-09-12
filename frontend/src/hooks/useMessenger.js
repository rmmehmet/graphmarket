import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { getConversationDetail, importExport, listConversations, triggerSync } from '@satgit/api-client'

export function useConversations(filters = {}) {
  return useQuery({
    queryKey: ['messenger-conversations', filters],
    queryFn: () => listConversations(filters),
  })
}

export function useConversationDetail(customer, product) {
  return useQuery({
    queryKey: ['messenger-conversation-detail', customer, product],
    queryFn: () => getConversationDetail(customer, product),
    enabled: Boolean(customer && product),
  })
}

export function useImportExport() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ file, channelId }) => importExport(file, channelId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['messenger-conversations'] }),
  })
}

export function useTriggerSync() {
  return useMutation({ mutationFn: triggerSync })
}
