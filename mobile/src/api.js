import { configureApiClient } from '@satgit/api-client'
import { authStore } from './authStore'

// Gerçek cihaz (Expo Go) makinenin LAN IP'sine bağlanmalı — telefon ve bilgisayar
// aynı Wi-Fi'de olmalı. Android emülatör: 10.0.2.2, iOS simülatör: localhost.
export const API_BASE_URL = 'http://192.168.1.106:8000'

configureApiClient({
  baseURL: API_BASE_URL,
  authStore: {
    getAccessToken: authStore.getAccessToken,
    getRefreshToken: authStore.getRefreshToken,
    setTokens: authStore.setTokens,
    clearTokens: authStore.clearTokens,
  },
})
