import { configureApiClient } from '@satgit/api-client'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { useUiStore } from './store/uiStore'

configureApiClient({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
  authStore: {
    getAccessToken: () => useUiStore.getState().accessToken,
    getRefreshToken: () => useUiStore.getState().refreshToken,
    setTokens: (accessToken, refreshToken) => useUiStore.getState().setTokens(accessToken, refreshToken),
    clearTokens: () => useUiStore.getState().clearTokens(),
  },
})

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
