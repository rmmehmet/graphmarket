import { useState } from 'react'
import JobStatusBadge from '../../components/ui/JobStatusBadge'
import useJobStatus from '../../hooks/useJobStatus'
import { useProducts } from '../../hooks/useProducts'
import { startResearch } from '@satgit/api-client'
import MarketResult from './MarketResult'

export default function MarketResearch() {
  const { data: products = [] } = useProducts()
  const [category, setCategory] = useState('')
  const [productId, setProductId] = useState('')
  const [jobId, setJobId] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  const { job, status, progress } = useJobStatus(jobId)

  async function handleSubmit(e) {
    e.preventDefault()
    setSubmitting(true)
    try {
      const { job_id } = await startResearch({ category, productId })
      setJobId(job_id)
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
