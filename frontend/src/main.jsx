import { configureApiClient } from '@satgit/api-client'
import * as Sentry from '@sentry/react'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import ErrorBoundary from './components/ErrorBoundary.jsx'
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

if (import.meta.env.VITE_SENTRY_DSN) {
  Sentry.init({ dsn: import.meta.env.VITE_SENTRY_DSN, tracesSampleRate: 0.1 })
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
)
