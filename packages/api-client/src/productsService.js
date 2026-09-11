import { client } from './client'

export async function listProducts({ category, search } = {}) {
  const { data } = await client.get('/api/products/', { params: { category, search } })
  return data
}

export async function createProduct(payload) {
  const { data } = await client.post('/api/products/', payload)
  return data
}

export async function updateProduct(productId, payload) {
  const { data } = await client.put(`/api/products/${productId}`, payload)
  return data
}

export async function deleteProduct(productId) {
  await client.delete(`/api/products/${productId}`)
}
