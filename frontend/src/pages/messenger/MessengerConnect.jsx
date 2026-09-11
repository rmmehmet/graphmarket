import { useState } from 'react'
import FileUploadZone from '../../components/ui/FileUploadZone'
import { useChannels } from '../../hooks/useChannels'
import { useImportExport, useTriggerSync } from '../../hooks/useMessenger'
import { getConnectUrl } from '../../services/messengerService'
import ConversationList from './ConversationList'

export default function MessengerConnect() {
  const { data: channels = [] } = useChannels()
  const [channelId, setChannelId] = useState('')
  const [importResult, setImportResult] = useState(null)
  const [syncResult, setSyncResult] = useState(null)
  const [connecting, setConnecting] = useState(false)

  const importExport = useImportExport()
  const triggerSync = useTriggerSync()

  async function handleConnect() {
    setConnecting(true)
    try {
      const { redirect_url } = await getConnectUrl()
      window.location.href = redirect_url
    } finally {
      setConnecting(false)
    }
  }

  function handleFile(file) {
    setImportResult(null)
    importExport.mutate(
      { file, channelId: channelId || null },
      { onSuccess: (data) => setImportResult(data) },
    )
  }

  function handleSync() {
    setSyncResult(null)
    triggerSync.mutate(undefined, { onSuccess: (data) => setSyncResult(data) })
  }

  return (
    <div>
      <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 26 }}>Messenger</h2>

      <div
        style={{
          background: 'var(--surface)',
          border: '1px solid var(--line)',
          borderRadius: 'var(--r-md)',
          padding: 16,
          marginBottom: 16,
        }}
      >
        <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 18, marginTop: 0 }}>
          Sayfa bağlantısı (gerçek zamanlı)
        </h3>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <button onClick={handleConnect} disabled={connecting} style={buttonStyle}>
            Facebook Sayfası bağla
          </button>
          <button onClick={handleSync} disabled={triggerSync.isPending} style={ghostButtonStyle}>
            Senkronize et
          </button>
        </div>
        {syncResult && (
          <p style={{ fontSize: 12.5, color: 'var(--ink-2)', marginTop: 8 }}>
            job_id: {syncResult.job_id}
          </p>
        )}
      </div>

      <div
        style={{
          background: 'var(--surface)',
          border: '1px solid var(--line)',
          borderRadius: 'var(--r-md)',
          padding: 16,
          marginBottom: 16,
        }}
      >
        <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 18, marginTop: 0 }}>
          Geçmiş veri (tek seferlik export)
        </h3>
        <p style={{ fontSize: 12.5, color: 'var(--ink-2)' }}>
          Facebook "Bilgilerinizi İndirin" ile aldığın mesaj export JSON dosyasını yükle.
        </p>
        <select
          value={channelId}
          onChange={(e) => setChannelId(e.target.value)}
          style={{ ...inputStyle, marginBottom: 8 }}
        >
          <option value="">Kanal seç (opsiyonel — çıkarılan satışlar bu kanala bağlanır)</option>
          {channels.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
        <FileUploadZone accept=".json" onFileSelected={handleFile} disabled={importExport.isPending} />
        {importExport.isPending && <p>Yükleniyor...</p>}
        {importResult && (
          <p style={{ fontSize: 12.5, color: 'var(--good)', marginTop: 8 }}>
            {importResult.message_count} mesaj işlenmek üzere kuyruğa alındı (job_id: {importResult.job_id})
          </p>
        )}
      </div>

      <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 20 }}>Konuşmalar</h3>
      <ConversationList />
    </div>
  )
}

const inputStyle = {
  padding: '9px 12px',
  borderRadius: 'var(--r-sm)',
  border: '1px solid var(--line-strong)',
  width: '100%',
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
  padding: '9px 18px',
  borderRadius: 'var(--r-sm)',
  border: '1px solid var(--teal)',
  background: 'transparent',
  color: 'var(--teal)',
  cursor: 'pointer',
}
