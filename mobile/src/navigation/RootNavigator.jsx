import { createNativeStackNavigator } from '@react-navigation/native-stack'
import useAuthState from '../useAuthState'
import AgentChatScreen from '../screens/AgentChatScreen'
import DashboardScreen from '../screens/DashboardScreen'
import LoginScreen from '../screens/LoginScreen'
import ProductsScreen from '../screens/ProductsScreen'
import RegisterScreen from '../screens/RegisterScreen'

const Stack = createNativeStackNavigator()

export default function RootNavigator() {
  const { isAuthenticated } = useAuthState()

  if (!isAuthenticated) {
    return (
      <Stack.Navigator>
        <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
        <Stack.Screen name="Register" component={RegisterScreen} options={{ headerShown: false }} />
      </Stack.Navigator>
    )
  }

  return (
    <Stack.Navigator>
      <Stack.Screen name="Dashboard" component={DashboardScreen} options={{ title: 'Panel' }} />
      <Stack.Screen name="Products" component={ProductsScreen} options={{ title: 'Ürünler' }} />
      <Stack.Screen name="AgentChat" component={AgentChatScreen} options={{ title: 'Ajan' }} />
    </Stack.Navigator>
  )
}
