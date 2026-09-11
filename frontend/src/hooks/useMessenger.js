import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { importExport, listConversations, triggerSync } from '../services/messengerService'

export function useConversations(filters = {}) {
  return useQuery({
    queryKey: ['messenger-conversations', filters],
    queryFn: () => listConversations(filters),
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
