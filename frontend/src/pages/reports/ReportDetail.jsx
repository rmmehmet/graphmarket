import { formatCurrency, formatDate } from '../../lib/formatters'

function downloadReport(report) {
  const lines = [
    `Rapor: ${report.period_start} — ${report.period_end}`,
    '',
    report.content?.narrative ?? '',
  ]
  const blob = new Blob([lines.join('\n')], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `rapor-${report.period_start}-${report.period_end}.txt`
  a.click()
  URL.revokeObjectURL(url)
}

export default function ReportDetail({ report }) {
  if (!report) return null

  const generating = !report.content

  return (
    <div
      style={{
        background: 'var(--surface)',
        border: '1px solid var(--line)',
        borderRadius: 'var(--r-md)',
        padding: 16,
        marginBottom: 16,
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 18, marginTop: 0 }}>
          {formatDate(report.period_start)} — {formatDate(report.period_end)}
        </h3>
        {!generating && (
          <button onClick={() => downloadReport(report)} style={ghostButtonStyle}>
            İndir
          </button>
        )}
      </div>

      {generating ? (
        <p style={{ color: 'var(--ink-2)' }}>Oluşturuluyor...</p>
      ) : (
        <>
          <div style={{ display: 'flex', gap: 24, margin: '8px 0 16px' }}>
            <div>
              <div style={{ fontSize: 12.5, color: 'var(--ink-2)' }}>TOPLAM GELİR</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: 20 }}>
                {formatCurrency(report.content.summary.total_revenue)}
              </div>
            </div>
            <div>
              <div style={{ fontSize: 12.5, color: 'var(--ink-2)' }}>SATILAN ADET</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: 20 }}>
                {report.content.summary.total_quantity}
              </div>
            </div>
          </div>
          <p style={{ whiteSpace: 'pre-wrap', fontSize: 14, lineHeight: 1.6 }}>
            {report.content.narrative}
          </p>
        </>
      )}
    </div>
  )
}

const ghostButtonStyle = {
  border: '1px solid var(--teal)',
  background: 'transparent',
  color: 'var(--teal)',
  borderRadius: 'var(--r-sm)',
  padding: '6px 13px',
  cursor: 'pointer',
}
