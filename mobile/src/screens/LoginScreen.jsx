import { login } from '@satgit/api-client'
import { useState } from 'react'
import { ActivityIndicator, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native'
import { authStore } from '../authStore'

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit() {
    setError(null)
    setSubmitting(true)
    try {
      const { access_token, refresh_token } = await login({ email, password })
      authStore.setTokens(access_token, refresh_token)
    } catch {
      setError('E-posta veya şifre hatalı.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>SatGit</Text>
      <TextInput
        style={styles.input}
        placeholder="E-posta"
        autoCapitalize="none"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        style={styles.input}
        placeholder="Şifre"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      {error && <Text style={styles.error}>{error}</Text>}
      <TouchableOpacity style={styles.button} onPress={handleSubmit} disabled={submitting}>
        {submitting ? <ActivityIndicator color="#1A1206" /> : <Text style={styles.buttonText}>Giriş yap</Text>}
      </TouchableOpacity>
      <TouchableOpacity onPress={() => navigation.navigate('Register')}>
        <Text style={styles.link}>Hesabın yok mu? Kayıt ol</Text>
      </TouchableOpacity>
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 24, backgroundColor: '#F1F4F1' },
  title: { fontSize: 34, fontWeight: '600', marginBottom: 24, color: '#16232B' },
  input: {
    borderWidth: 1,
    borderColor: '#C3CDC6',
    borderRadius: 6,
    padding: 12,
    marginBottom: 12,
    backgroundColor: '#FFFFFF',
  },
  button: { backgroundColor: '#E08E1D', borderRadius: 6, padding: 12, alignItems: 'center', marginTop: 8 },
  buttonText: { color: '#1A1206', fontWeight: '600' },
  error: { color: '#d03b3b', marginBottom: 8 },
  link: { color: '#1F6F6B', marginTop: 16, textAlign: 'center' },
})
