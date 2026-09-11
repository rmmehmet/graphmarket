import { client } from './client'

export async function listChannels() {
  const { data } = await client.get('/api/channels/')
  return data
}

export async function createChannel(payload) {
  const { data } = await client.post('/api/channels/', payload)
  return data
}

export async function updateChannel(channelId, payload) {
  const { data } = await client.put(`/api/channels/${channelId}`, payload)
  return data
}

export async function deleteChannel(channelId) {
  await client.delete(`/api/channels/${channelId}`)
}
