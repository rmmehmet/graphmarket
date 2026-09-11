import { useEffect, useState } from 'react'
import { authStore } from './authStore'

export default function useAuthState() {
  const [state, setState] = useState(authStore.getState())

  useEffect(() => authStore.subscribe(setState), [])

  return { isAuthenticated: Boolean(state.accessToken) }
}
