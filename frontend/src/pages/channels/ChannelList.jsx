import { useState } from 'react'
import { useChannels, useCreateChannel, useDeleteChannel } from '../../hooks/useChannels'

export default function ChannelList() {
  const { data: channels = [], isLoading } = useChannels()
  const createChannel = useCreateChannel()
  const deleteChannel = useDeleteChannel()

  const [name, setName] = useState('')
  const [platform, setPlatform] = useState('facebook_group')

  function handleSubmit(e) {
    e.preventDefault()
    createChannel.mutate({ name, platform }, { onSuccess: () => setName('') })
  }

  return (
    <div>
      <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 26 }}>Kanallar</h2>

      <form
        onSubmit={handleSubmit}
        style={{ display: 'flex', gap: 8, margin: '16px 0', flexWrap: 'wrap' }}
      >
        <input
          placeholder="Kanal adı"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={inputStyle}
        />
        <select value={platform} onChange={(e) => setPlatform(e.target.value)} style={inputStyle}>
          <option value="facebook_group">Facebook Grubu</option>
          <option value="instagram">Instagram</option>
          <option value="trendyol">Trendyol</option>
          <option value="other">Diğer</option>
        </select>
        <button type="submit" disabled={createChannel.isPending} style={buttonStyle}>
          Ekle
        </button>
      </form>

      {isLoading ? (
        <p>Yükleniyor...</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--line)' }}>
              <th style={thStyle}>Ad</th>
              <th style={thStyle}>Platform</th>
              <th style={thStyle} />
            </tr>
          </thead>
          <tbody>
            {channels.map((c) => (
              <tr key={c.id} style={{ borderBottom: '1px solid var(--line)' }}>
                <td style={tdStyle}>{c.name}</td>
                <td style={tdStyle}>{c.platform}</td>
                <td style={tdStyle}>
                  <button onClick={() => deleteChannel.mutate(c.id)} style={ghostButtonStyle}>
                    Sil
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
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

const ghostButtonStyle = {
  border: 'none',
  background: 'none',
  color: 'var(--critical)',
  cursor: 'pointer',
}

const thStyle = { textAlign: 'left', padding: '8px 4px', color: 'var(--ink-2)', fontSize: 12.5 }
const tdStyle = { padding: '8px 4px' }
