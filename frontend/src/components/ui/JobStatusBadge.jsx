const STATUS_META = {
  queued: { color: 'var(--ink-mute)', label: 'Sırada' },
  running: { color: 'var(--warning)', label: 'Çalışıyor' },
  done: { color: 'var(--good)', label: 'Tamamlandı' },
  error: { color: 'var(--critical)', label: 'Hata' },
}

export default function JobStatusBadge({ status }) {
  const meta = STATUS_META[status] ?? STATUS_META.queued

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        padding: '4px 10px',
        borderRadius: 'var(--r-pill)',
        background: `color-mix(in srgb, ${meta.color} 18%, transparent)`,
        color: meta.color,
        fontSize: 12.5,
        fontWeight: 500,
      }}
    >
      <span style={{ width: 6, height: 6, borderRadius: '50%', background: meta.color }} />
      {meta.label}
    </span>
  )
}
