export default function Topbar() {
  return (
    <header
      style={{
        height: 56,
        borderBottom: '1px solid var(--line)',
        display: 'flex',
        alignItems: 'center',
        padding: '0 16px',
        background: 'var(--surface)',
      }}
    >
      <span style={{ fontFamily: 'var(--font-display)', fontWeight: 560, fontSize: 20 }}>
        SatGit
      </span>
    </header>
  )
}
