import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import useAuth from '../../hooks/useAuth'
import { login, register } from '../../services/authService'

export default function Register() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [businessName, setBusinessName] = useState('')
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const { setTokens } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setSubmitting(true)
    try {
      await register({ email, password, businessName })
      const { access_token, refresh_token } = await login({ email, password })
      setTokens(access_token, refresh_token)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail ?? 'Kayıt oluşturulamadı.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div style={{ maxWidth: 360, margin: '80px auto', padding: 24 }}>
      <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 34 }}>SatGit</h1>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <input
          type="text"
          placeholder="İşletme adı"
          value={businessName}
          onChange={(e) => setBusinessName(e.target.value)}
          style={inputStyle}
        />
        <input
          type="email"
          placeholder="E-posta"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={inputStyle}
        />
        <input
          type="password"
          placeholder="Şifre"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={inputStyle}
        />
        {error && <span style={{ color: 'var(--critical)', fontSize: 13 }}>{error}</span>}
        <button type="submit" disabled={submitting} style={buttonStyle}>
          {submitting ? 'Kayıt oluşturuluyor...' : 'Kayıt ol'}
        </button>
      </form>
      <p style={{ marginTop: 16, fontSize: 13, color: 'var(--ink-2)' }}>
        Zaten hesabın var mı? <Link to="/login">Giriş yap</Link>
      </p>
    </div>
  )
}

const inputStyle = {
  padding: '9px 12px',
  borderRadius: 'var(--r-sm)',
  border: '1px solid var(--line-strong)',
  fontFamily: 'var(--font-body)',
}

const buttonStyle = {
  padding: '9px 18px',
  borderRadius: 'var(--r-sm)',
  border: 'none',
  background: 'var(--accent)',
  color: 'var(--on-accent)',
  fontWeight: 600,
  cursor: 'pointer',
}
