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
    const isAuthEndpoint = error.config?.url?.startsWith('/api/auth/')
    if (error.response?.status === 401 && !error.config._retried && !isAuthEndpoint) {
      error.config._retried = true
      const { refreshToken, setTokens, clearTokens } = useUiStore.getState()
      if (!refreshToken) {
        clearTokens()
        return Promise.reject(error)
      }
      try {
        refreshPromise ??= client
          .post('/api/auth/refresh', { refresh_token: refreshToken })
          .finally(() => {
            refreshPromise = null
          })
        const { data } = await refreshPromise
        setTokens(data.access_token, refreshToken)
        return client(error.config)
      } catch (refreshError) {
        clearTokens()
        return Promise.reject(refreshError)
      }
    }
    return Promise.reject(error)
  },
)

export default client
