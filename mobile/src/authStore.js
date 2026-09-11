import AsyncStorage from '@react-native-async-storage/async-storage'

const STORAGE_KEY = 'satgit-auth'

let state = { accessToken: null, refreshToken: null }
let listeners = []

function notify() {
  listeners.forEach((fn) => fn(state))
}

function persist() {
  AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(state)).catch(() => {})
}

async function init() {
  try {
    const raw = await AsyncStorage.getItem(STORAGE_KEY)
    if (raw) {
      state = JSON.parse(raw)
      notify()
    }
  } catch {
    // depolama okunamadıysa oturumsuz devam edilir
  }
}

export const authStore = {
  init,
  getState: () => state,
  getAccessToken: () => state.accessToken,
  getRefreshToken: () => state.refreshToken,
  setTokens: (accessToken, refreshToken) => {
    state = { accessToken, refreshToken }
    persist()
    notify()
  },
  clearTokens: () => {
    state = { accessToken: null, refreshToken: null }
    persist()
    notify()
  },
  subscribe: (fn) => {
    listeners.push(fn)
    return () => {
      listeners = listeners.filter((l) => l !== fn)
    }
  },
}
