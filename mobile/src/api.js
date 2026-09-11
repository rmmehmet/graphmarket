import { configureApiClient } from '@satgit/api-client'
import { authStore } from './authStore'

// Android emülatör: 10.0.2.2, iOS simülatör: localhost, gerçek cihaz: makinenin LAN IP'si.
export const API_BASE_URL = 'http://10.0.2.2:8000'

configureApiClient({
  baseURL: API_BASE_URL,
  authStore: {
    getAccessToken: authStore.getAccessToken,
    getRefreshToken: authStore.getRefreshToken,
    setTokens: authStore.setTokens,
    clearTokens: authStore.clearTokens,
  },
})
