import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useEffect, useRef } from 'react'
import { getJob, jobWebSocketUrl } from '@satgit/api-client'

const TERMINAL_STATUSES = new Set(['done', 'error'])

export default function useJobStatus(jobId) {
  const queryClient = useQueryClient()
  const wsConnectedRef = useRef(false)

  const query = useQuery({
    queryKey: ['job', jobId],
    queryFn: () => getJob(jobId),
    enabled: Boolean(jobId),
    refetchInterval: (q) => {
      if (wsConnectedRef.current) return false
      const data = q.state.data
      if (!data || TERMINAL_STATUSES.has(data.status)) return false
      return 2000
    },
  })

  useEffect(() => {
    if (!jobId) return

    const ws = new WebSocket(jobWebSocketUrl(jobId))

    ws.onopen = () => {
      wsConnectedRef.current = true
    }

    ws.onmessage = (event) => {
      const payload = JSON.parse(event.data)
      queryClient.setQueryData(['job', jobId], (prev) => ({ ...prev, ...payload }))
    }

    ws.onclose = () => {
      wsConnectedRef.current = false
    }

    return () => {
      wsConnectedRef.current = false
      ws.close()
    }
  }, [jobId, queryClient])

  return {
    job: query.data,
    status: query.data?.status,
    progress: query.data?.progress ?? 0,
    isLoading: query.isLoading,
  }
}
