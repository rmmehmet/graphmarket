import './src/api'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { NavigationContainer } from '@react-navigation/native'
import { StatusBar } from 'expo-status-bar'
import { useEffect, useState } from 'react'
import { ActivityIndicator, View } from 'react-native'
import RootNavigator from './src/navigation/RootNavigator'
import { authStore } from './src/authStore'

const queryClient = new QueryClient()

export default function App() {
  const [ready, setReady] = useState(false)

  useEffect(() => {
    authStore.init().finally(() => setReady(true))
  }, [])

  if (!ready) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator />
      </View>
    )
  }

  return (
    <QueryClientProvider client={queryClient}>
      <NavigationContainer>
        <RootNavigator />
      </NavigationContainer>
      <StatusBar style="auto" />
    </QueryClientProvider>
  )
}
