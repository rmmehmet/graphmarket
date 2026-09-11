import { useUiStore } from '../store/uiStore'

export default function useAuth() {
  const accessToken = useUiStore((s) => s.accessToken)
  const setTokens = useUiStore((s) => s.setTokens)
  const clearTokens = useUiStore((s) => s.clearTokens)
  return { isAuthenticated: Boolean(accessToken), setTokens, logout: clearTokens }
}
