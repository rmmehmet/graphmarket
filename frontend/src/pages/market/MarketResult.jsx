export default function MarketResult({ result }) {
  if (!result) return null

  return (
    <div
      style={{
        background: 'var(--surface)',
        border: '1px solid var(--line)',
        borderRadius: 'var(--r-md)',
        padding: 16,
        marginTop: 16,
      }}
    >
      <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 20, marginTop: 0 }}>
        {result.category}
      </h3>
      <p style={{ whiteSpace: 'pre-wrap', fontSize: 14, lineHeight: 1.6 }}>{result.text}</p>
      <p style={{ fontSize: 12.5, color: 'var(--ink-2)' }}>{result.sources} kaynaktan derlendi</p>
    </div>
  )
}
