import { client, getBaseURL } from './client'

export async function getJob(jobId) {
  const { data } = await client.get(`/api/jobs/${jobId}`)
  return data
}

export function jobWebSocketUrl(jobId) {
  const wsBase = getBaseURL().replace(/^http/, 'ws')
  return `${wsBase}/ws/jobs/${jobId}`
}
