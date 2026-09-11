import { client } from './client'

export async function getModelProfiles() {
  const { data } = await client.get('/api/settings/model-profile')
  return data
}

export async function updateModelProfile(payload) {
  const { data } = await client.put('/api/settings/model-profile', payload)
  return data
}

export async function testModelProfile(node) {
  const { data } = await client.post('/api/settings/model-profile/test', { node })
  return data
}
