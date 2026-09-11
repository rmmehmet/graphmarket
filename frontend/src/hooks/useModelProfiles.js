import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { getModelProfiles, testModelProfile, updateModelProfile } from '@satgit/api-client'

export function useModelProfiles() {
  return useQuery({ queryKey: ['model-profiles'], queryFn: getModelProfiles })
}

export function useUpdateModelProfile() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: updateModelProfile,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['model-profiles'] }),
  })
}

export function useTestModelProfile() {
  return useMutation({ mutationFn: testModelProfile })
}
