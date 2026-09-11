import { useState } from 'react'
import { useChannels } from '../../hooks/useChannels'
import { useGenerateReport, useReports } from '../../hooks/useReports'
import ReportDetail from './ReportDetail'

function firstDayOfMonth() {
  const d = new Date()
  return new Date(d.getFullYear(), d.getMonth(), 1).toISOString().slice(0, 10)
}

function today() {
  return new Date().toISOString().slice(0, 10)
}

export default function ReportList() {
  const { data: reports = [], isLoading, refetch } = useReports()
  const { data: channels = [] } = useChannels()
  const generateReport = useGenerateReport()

  const [periodStart, setPeriodStart] = useState(firstDayOfMonth())
  const [periodEnd, setPeriodEnd] = useState(today())
  const [channelId, setChannelId] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    generateReport.mutate(
      {
        type: 'sales_summary',
        periodStart,
        periodEnd,
        channelIds: channelId ? [channelId] : [],
      },
      {
        onSuccess: () => {
          setTimeout(() => refetch(), 8000)
        },
      },
    )
  }

  return (
    <div>
      <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 26 }}>Raporlar</h2>

      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8, margin: '16px 0', flexWrap: 'wrap' }}>
        <input
          type="date"
          value={periodStart}
          onChange={(e) => setPeriodStart(e.target.value)}
          style={inputStyle}
        />
        <input
          type="date"
          value={periodEnd}
          onChange={(e) => setPeriodEnd(e.target.value)}
          style={inputStyle}
        />
        <select value={channelId} onChange={(e) => setChannelId(e.target.value)} style={inputStyle}>
          <option value="">Tüm kanallar</option>
          {channels.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
        <button type="submit" disabled={generateReport.isPending} style={buttonStyle}>
          Rapor oluştur
        </button>
      </form>

      {isLoading ? (
        <p>Yükleniyor...</p>
      ) : reports.length === 0 ? (
        <p style={{ color: 'var(--ink-2)', fontSize: 13 }}>Henüz rapor yok.</p>
      ) : (
        reports.map((r) => <ReportDetail key={r.id} report={r} />)
      )}
    </div>
  )
}

const inputStyle = {
  padding: '9px 12px',
  borderRadius: 'var(--r-sm)',
  border: '1px solid var(--line-strong)',
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
