import axios from 'axios'

export const client = axios.create()

let authStore = {
  getAccessToken: () => null,
  getRefreshToken: () => null,
  setTokens: () => {},
  clearTokens: () => {},
}

let baseURL = ''

/**
 * Web (Vite) ve React Native, farklı token depolama (localStorage/persist vs AsyncStorage)
 * ve farklı env okuma yolları (import.meta.env vs process.env) kullanır — bu yüzden client
 * kendi başına hiçbirini bilmez, host uygulama başlangıçta bunu çağırıp bağlar.
 */
export function configureApiClient({ baseURL: url, authStore: store }) {
  baseURL = url
  client.defaults.baseURL = url
  if (store) authStore = store
}

export function getBaseURL() {
  return baseURL
}

client.interceptors.request.use((config) => {
  const token = authStore.getAccessToken()
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
      const refreshToken = authStore.getRefreshToken()
      if (!refreshToken) {
        authStore.clearTokens()
        return Promise.reject(error)
      }
      try {
        refreshPromise ??= client
          .post('/api/auth/refresh', { refresh_token: refreshToken })
          .finally(() => {
            refreshPromise = null
          })
        const { data } = await refreshPromise
        authStore.setTokens(data.access_token, refreshToken)
        return client(error.config)
      } catch (refreshError) {
        authStore.clearTokens()
        return Promise.reject(refreshError)
      }
    }
    return Promise.reject(error)
  },
)
