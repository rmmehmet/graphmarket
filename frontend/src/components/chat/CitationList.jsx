export default function CitationList({ citations }) {
  if (!citations?.length) return null

  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 6 }}>
      {citations.map((c, i) => (
        <span
          key={i}
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: 11.5,
            background: 'var(--surface)',
            border: '1px solid var(--line)',
            borderRadius: 'var(--r-sm)',
            padding: '2px 8px',
          }}
        >
          {c.label}
        </span>
      ))}
    </div>
  )
}
