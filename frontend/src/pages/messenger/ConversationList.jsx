import { useState } from 'react'
import { useConversationDetail, useConversations } from '../../hooks/useMessenger'
import { formatDate } from '../../lib/formatters'

export default function ConversationList() {
  const { data: conversations = [], isLoading } = useConversations()
  const [selected, setSelected] = useState(null)

  if (isLoading) return <p>Yükleniyor...</p>

  if (!conversations.length) {
    return <p style={{ color: 'var(--ink-2)', fontSize: 13 }}>Henüz eşleşen konuşma yok.</p>
  }

  return (
    <div>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid var(--line)' }}>
            <th style={thStyle}>Müşteri</th>
            <th style={thStyle}>Ürün</th>
            <th style={thStyle}>Duygu</th>
            <th style={thStyle}>Tarih</th>
          </tr>
        </thead>
        <tbody>
          {conversations.map((c, i) => (
            <tr
              key={i}
              onClick={() => c.product && setSelected(c)}
              style={{
                borderBottom: '1px solid var(--line)',
                cursor: c.product ? 'pointer' : 'default',
                background: selected === c ? 'var(--surface-2, #f3f3f0)' : 'transparent',
              }}
            >
              <td style={{ ...tdStyle, fontFamily: 'var(--font-mono)' }}>{c.customer}</td>
              <td style={tdStyle}>{c.product ?? '—'}</td>
              <td style={tdStyle}>{c.sentiment ?? '—'}</td>
              <td style={tdStyle}>{formatDate(c.mentioned_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {selected && (
        <ConversationDetailPanel
          customer={selected.customer}
          product={selected.product}
          onClose={() => setSelected(null)}
        />
      )}
    </div>
  )
}

function ConversationDetailPanel({ customer, product, onClose }) {
  const { data: detail, isLoading, isError } = useConversationDetail(customer, product)

  return (
    <div
      style={{
        marginTop: 12,
        border: '1px solid var(--line)',
        borderRadius: 'var(--r-md)',
        padding: 16,
        background: 'var(--surface)',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h4 style={{ margin: 0, fontFamily: 'var(--font-display)', fontSize: 16 }}>
          {customer} · {product}
        </h4>
        <button onClick={onClose} style={closeButtonStyle}>
          Kapat
        </button>
      </div>

      {!product && (
        <p style={{ fontSize: 13, color: 'var(--ink-2)' }}>Bu müşteri için eşleşen ürün yok, detay gösterilemiyor.</p>
      )}
      {product && isLoading && <p style={{ fontSize: 13 }}>Yükleniyor...</p>}
      {product && isError && <p style={{ fontSize: 13, color: 'var(--critical)' }}>Detay yüklenemedi.</p>}

      {detail && (
        <ul style={{ marginTop: 12, paddingLeft: 0, listStyle: 'none' }}>
          {detail.messages.length === 0 && (
            <li style={{ fontSize: 13, color: 'var(--ink-2)' }}>Bu konuşma için kayıtlı mesaj yok.</li>
          )}
          {detail.messages.map((text, i) => (
            <li
              key={i}
              style={{
                fontSize: 13.5,
                padding: '8px 12px',
                marginBottom: 6,
                background: 'var(--bg, #f7f6f2)',
                borderRadius: 'var(--r-sm)',
              }}
            >
              {text}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

const thStyle = { textAlign: 'left', padding: '8px 4px', color: 'var(--ink-2)', fontSize: 12.5 }
const tdStyle = { padding: '8px 4px' }
const closeButtonStyle = {
  padding: '4px 10px',
  borderRadius: 'var(--r-sm)',
  border: '1px solid var(--line-strong)',
  background: 'transparent',
  cursor: 'pointer',
  fontSize: 12.5,
}
