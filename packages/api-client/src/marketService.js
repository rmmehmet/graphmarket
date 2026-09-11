import { client } from './client'

export async function startResearch({ category, productId }) {
  const { data } = await client.post('/api/market/research', {
    category,
    product_id: productId || null,
  })
  return data
}

export async function getResearchResult(jobId) {
  const { data } = await client.get(`/api/market/research/${jobId}`)
  return data
}

export async function listTrends(category) {
  const { data } = await client.get('/api/market/trends', { params: { category } })
  return data
}
