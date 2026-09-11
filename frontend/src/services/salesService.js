import client from './client'

export async function listSales({ productId, channelId, dateFrom, dateTo } = {}) {
  const { data } = await client.get('/api/sales/', {
    params: {
      product_id: productId,
      channel_id: channelId,
      date_from: dateFrom,
      date_to: dateTo,
    },
  })
  return data
}

export async function createSale(payload) {
  const { data } = await client.post('/api/sales/', payload)
  return data
}

export async function getSalesAnalytics(groupBy = 'week') {
  const { data } = await client.get('/api/sales/analytics', { params: { group_by: groupBy } })
  return data
}

export async function importSales(file) {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await client.post('/api/sales/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}
