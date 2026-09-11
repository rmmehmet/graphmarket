export default function StatCard({ label, value, delta }) {
  return (
    <div
      style={{
        background: 'var(--surface)',
        border: '1px solid var(--line)',
        borderRadius: 'var(--r-md)',
        padding: 16,
        minWidth: 160,
      }}
    >
      <div
        style={{
          fontFamily: 'var(--font-body)',
          fontWeight: 500,
          fontSize: 12.5,
          letterSpacing: '0.02em',
          textTransform: 'uppercase',
          color: 'var(--ink-2)',
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontFamily: 'var(--font-mono)',
          fontWeight: 500,
          fontSize: 26,
          marginTop: 4,
        }}
      >
        {value}
      </div>
      {delta && <div style={{ color: 'var(--good)', fontSize: 12.5, marginTop: 4 }}>{delta}</div>}
    </div>
  )
}
