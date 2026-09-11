import axios from 'axios'
import { useUiStore } from '../store/uiStore'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
})

client.interceptors.request.use((config) => {
  const token = useUiStore.getState().accessToken
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

let refreshPromise = null

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retried) {
      error.config._retried = true
      refreshPromise ??= client.post('/api/auth/refresh').finally(() => {
        refreshPromise = null
      })
      await refreshPromise
      return client(error.config)
    }
    return Promise.reject(error)
  },
)

export default client
