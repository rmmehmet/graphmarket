import { useConversations } from '../../hooks/useMessenger'
import { formatDate } from '../../lib/formatters'

export default function ConversationList() {
  const { data: conversations = [], isLoading } = useConversations()

  if (isLoading) return <p>Yükleniyor...</p>

  if (!conversations.length) {
    return <p style={{ color: 'var(--ink-2)', fontSize: 13 }}>Henüz eşleşen konuşma yok.</p>
  }

  return (
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
          <tr key={i} style={{ borderBottom: '1px solid var(--line)' }}>
            <td style={{ ...tdStyle, fontFamily: 'var(--font-mono)' }}>{c.customer}</td>
            <td style={tdStyle}>{c.product ?? '—'}</td>
            <td style={tdStyle}>{c.sentiment ?? '—'}</td>
            <td style={tdStyle}>{formatDate(c.mentioned_at)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

const thStyle = { textAlign: 'left', padding: '8px 4px', color: 'var(--ink-2)', fontSize: 12.5 }
const tdStyle = { padding: '8px 4px' }
