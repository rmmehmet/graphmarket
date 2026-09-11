import { client } from './client'

export async function getConnectUrl() {
  const { data } = await client.get('/api/messenger/connect')
  return data
}

export async function importExport(file, channelId) {
  const formData = new FormData()
  formData.append('file', file)
  if (channelId) formData.append('channel_id', channelId)
  const { data } = await client.post('/api/messenger/import-export', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function triggerSync() {
  const { data } = await client.post('/api/messenger/sync')
  return data
}

export async function listConversations({ customer, productHint } = {}) {
  const { data } = await client.get('/api/messenger/conversations', {
    params: { customer, product_hint: productHint },
  })
  return data
}
