import { useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import JobStatusBadge from '../../components/ui/JobStatusBadge'
import useJobStatus from '../../hooks/useJobStatus'
import useJobsList from '../../hooks/useJobsList'
import { useProducts } from '../../hooks/useProducts'
import { formatDate } from '../../lib/formatters'
import { startResearch } from '@satgit/api-client'
import MarketResult from './MarketResult'

export default function MarketResearch() {
  const queryClient = useQueryClient()
  const { data: products = [] } = useProducts()
  const [category, setCategory] = useState('')
  const [productId, setProductId] = useState('')
  const [jobId, setJobId] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  const { job, status, progress } = useJobStatus(jobId)
  const { data: history = [] } = useJobsList('trend_research')

  async function handleSubmit(e) {
    e.preventDefault()
    setSubmitting(true)
    try {
      const { job_id } = await startResearch({ category, productId })
      setJobId(job_id)
      queryClient.invalidateQueries({ queryKey: ['jobs', 'trend_research'] })
    } finally {
      setSubmitting(false)
    }
  }

  let result = null
  if (job?.result_ref) {
    try {
      result = JSON.parse(job.result_ref)
    } catch {
      result = null
    }
  }

  function openHistoryEntry(entry) {
    setJobId(entry.id)
  }

  return (
    <div>
      <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 26 }}>Pazar / Trend</h2>

      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8, margin: '16px 0', flexWrap: 'wrap' }}>
        <input
          placeholder="Kategori (örn. el yapımı takı)"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          required
          style={inputStyle}
        />
        <select value={productId} onChange={(e) => setProductId(e.target.value)} style={inputStyle}>
          <option value="">Ürün seç (opsiyonel)</option>
          {products.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        <button type="submit" disabled={submitting} style={buttonStyle}>
          Araştırmayı başlat
        </button>
      </form>

      {jobId && (
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <JobStatusBadge status={status} />
          {status && status !== 'done' && status !== 'error' && (
            <span style={{ fontSize: 12.5, color: 'var(--ink-2)' }}>%{progress}</span>
          )}
        </div>
      )}

      {status === 'error' && (
        <p style={{ color: 'var(--critical)', fontSize: 13 }}>{job?.error_message}</p>
      )}

      <MarketResult result={result} />

      <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 20, marginTop: 32 }}>Geçmiş</h3>
      {history.length === 0 ? (
        <p style={{ color: 'var(--ink-2)', fontSize: 13 }}>Henüz araştırma çalıştırılmadı.</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--line)' }}>
              <th style={thStyle}>Kategori</th>
              <th style={thStyle}>Durum</th>
              <th style={thStyle}>Tarih</th>
            </tr>
          </thead>
          <tbody>
            {history.map((entry) => (
              <tr
                key={entry.id}
                onClick={() => openHistoryEntry(entry)}
                style={{
                  borderBottom: '1px solid var(--line)',
                  cursor: 'pointer',
                  background: jobId === entry.id ? 'var(--surface-2, #f3f3f0)' : 'transparent',
                }}
              >
                <td style={tdStyle}>{entry.input_payload?.category ?? '—'}</td>
                <td style={tdStyle}>
                  <JobStatusBadge status={entry.status} />
                </td>
                <td style={tdStyle}>{formatDate(entry.created_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

const thStyle = { textAlign: 'left', padding: '8px 4px', color: 'var(--ink-2)', fontSize: 12.5 }
const tdStyle = { padding: '8px 4px' }

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
