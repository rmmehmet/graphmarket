import { client } from './client'

export async function askAgent({ question, contextProductId }) {
  const { data } = await client.post('/api/agent/ask', {
    question,
    context_product_id: contextProductId || null,
  })
  return data
}

export async function askAgentDeep(question) {
  const { data } = await client.post('/api/agent/ask-deep', { question })
  return data
}

export async function getAgentHistory(limit = 20) {
  const { data } = await client.get('/api/agent/history', { params: { limit } })
  return data
}
