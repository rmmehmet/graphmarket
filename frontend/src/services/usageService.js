import client from './client'

export async function getUsage() {
  const { data } = await client.get('/api/usage/')
  return data
}
