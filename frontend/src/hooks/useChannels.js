import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  createChannel,
  deleteChannel,
  listChannels,
  updateChannel,
} from '@satgit/api-client'

export function useChannels() {
  return useQuery({ queryKey: ['channels'], queryFn: listChannels })
}

export function useCreateChannel() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: createChannel,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['channels'] }),
  })
}

export function useUpdateChannel() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ channelId, payload }) => updateChannel(channelId, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['channels'] }),
  })
}

export function useDeleteChannel() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: deleteChannel,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['channels'] }),
  })
}
