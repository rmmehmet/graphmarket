import { useUiStore } from '../store/uiStore'

export default function useAuth() {
  const token = useUiStore((s) => s.accessToken)
  return { isAuthenticated: Boolean(token) }
}
