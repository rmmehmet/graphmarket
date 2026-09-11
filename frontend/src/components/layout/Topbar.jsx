import { useNavigate } from 'react-router-dom'
import useAuth from '../../hooks/useAuth'

export default function Topbar() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <header
      style={{
        height: 56,
        borderBottom: '1px solid var(--line)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 16px',
        background: 'var(--surface)',
      }}
    >
      <span style={{ fontFamily: 'var(--font-display)', fontWeight: 560, fontSize: 20 }}>
        SatGit
      </span>
      <button
        onClick={handleLogout}
        style={{
          border: 'none',
          background: 'none',
          color: 'var(--ink-2)',
          cursor: 'pointer',
        }}
      >
        Çıkış yap
      </button>
    </header>
  )
}
