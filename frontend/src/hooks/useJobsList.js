import { useQuery } from '@tanstack/react-query'
import { listJobs } from '@satgit/api-client'

export default function useJobsList(type, limit = 50) {
  return useQuery({
    queryKey: ['jobs', type, limit],
    queryFn: () => listJobs({ type, limit }),
  })
}
