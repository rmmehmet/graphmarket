const JOB_TYPE_LABELS = {
  trend_research: 'Pazar Araştırması',
  agent_ask_deep: 'Derin Ajan Sorgusu',
  messenger_sync: 'Messenger Senkronizasyon',
}

function UsageBar({ item }) {
  const { job_type, used, limit } = item
  const label = JOB_TYPE_LABELS[job_type] ?? job_type

  if (limit === null) {
    return (
      <div style={{ marginBottom: 12 }}>
        <div style={rowStyle}>
          <span>{label}</span>
          <span style={{ color: 'var(--ink-2)' }}>{used} · sınırsız</span>
        </div>
      </div>
    )
  }

  const pct = limit > 0 ? Math.min((used / limit) * 100, 100) : 100
  const nearLimit = pct > 80

  return (
    <div style={{ marginBottom: 12 }}>
      <div style={rowStyle}>
        <span>{label}</span>
        <span style={{ color: 'var(--ink-2)', fontFamily: 'var(--font-mono)' }}>
          {used} / {limit}
        </span>
      </div>
      <div
        style={{
          height: 6,
          borderRadius: 'var(--r-pill)',
          background: 'var(--surface-2)',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            height: '100%',
            width: `${pct}%`,
            background: nearLimit ? 'var(--warning)' : 'var(--teal)',
            transition: 'width 0.2s',
          }}
        />
      </div>
      {nearLimit && (
        <p style={{ fontSize: 11.5, color: 'var(--warning)', margin: '4px 0 0' }}>
          Limite yaklaşıyorsun
        </p>
      )}
    </div>
  )
}

export default function UsageMeter({ usage }) {
  if (!usage) return null

  return (
    <div
      style={{
        background: 'var(--surface)',
        border: '1px solid var(--line)',
        borderRadius: 'var(--r-md)',
        padding: 16,
      }}
    >
      <div
        style={{
          fontSize: 12.5,
          fontWeight: 500,
          letterSpacing: '0.02em',
          textTransform: 'uppercase',
          color: 'var(--ink-2)',
          marginBottom: 12,
        }}
      >
        Kullanım — {usage.plan} plan ({usage.period})
      </div>
      {usage.breakdown.map((item) => (
        <UsageBar key={item.job_type} item={item} />
      ))}
    </div>
  )
}

const rowStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  fontSize: 13,
  marginBottom: 4,
}
