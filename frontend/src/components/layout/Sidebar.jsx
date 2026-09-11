import { NavLink } from 'react-router-dom'

const NAV_ITEMS = [
  { to: '/dashboard', label: 'Panel' },
  { to: '/products', label: 'Ürünler' },
  { to: '/sales', label: 'Satışlar' },
  { to: '/channels', label: 'Kanallar' },
  { to: '/market', label: 'Pazar/Trend' },
  { to: '/messenger', label: 'Messenger' },
  { to: '/agent', label: 'Ajan' },
  { to: '/reports', label: 'Raporlar' },
  { to: '/settings', label: 'Ayarlar' },
]

export default function Sidebar() {
  return (
    <nav
      style={{
        width: 220,
        borderRight: '1px solid var(--line)',
        padding: 16,
        background: 'var(--surface)',
      }}
    >
      {NAV_ITEMS.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          style={({ isActive }) => ({
            display: 'block',
            padding: '8px 12px',
            borderRadius: 'var(--r-sm)',
            marginBottom: 4,
            textDecoration: 'none',
            fontWeight: isActive ? 600 : 400,
            color: isActive ? 'var(--accent-strong)' : 'var(--ink-2)',
            background: isActive ? 'var(--accent-soft)' : 'transparent',
          })}
        >
          {item.label}
        </NavLink>
      ))}
    </nav>
  )
}
