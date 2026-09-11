import client from './client'

export async function register({ email, password, businessName }) {
  const { data } = await client.post('/api/auth/register', {
    email,
    password,
    business_name: businessName,
  })
  return data
}

export async function login({ email, password }) {
  const { data } = await client.post('/api/auth/login', { email, password })
  return data
}

export async function me() {
  const { data } = await client.get('/api/auth/me')
  return data
}
