import { client } from './client'

export async function listReports() {
  const { data } = await client.get('/api/reports/')
  return data
}

export async function generateReport({ type, periodStart, periodEnd, channelIds }) {
  const { data } = await client.post('/api/reports/generate', {
    type,
    period: { start: periodStart, end: periodEnd },
    channel_ids: channelIds ?? [],
  })
  return data
}

export async function getReport(reportId) {
  const { data } = await client.get(`/api/reports/${reportId}`)
  return data
}
