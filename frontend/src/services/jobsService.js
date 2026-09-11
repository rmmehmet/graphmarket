import client from './client'

export async function getJob(jobId) {
  const { data } = await client.get(`/api/jobs/${jobId}`)
  return data
}

export function jobWebSocketUrl(jobId) {
  const base = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
  const wsBase = base.replace(/^http/, 'ws')
  return `${wsBase}/ws/jobs/${jobId}`
}
