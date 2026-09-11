import { getConnectUrl } from '@satgit/api-client'
import { useQueryClient } from '@tanstack/react-query'
import { useEffect, useState } from 'react'
import FileUploadZone from '../../components/ui/FileUploadZone'
import JobStatusBadge from '../../components/ui/JobStatusBadge'
import { useChannels } from '../../hooks/useChannels'
import useJobStatus from '../../hooks/useJobStatus'
import { useImportExport, useTriggerSync } from '../../hooks/useMessenger'
import ConversationList from './ConversationList'

export default function MessengerConnect() {
  const queryClient = useQueryClient()
  const { data: channels = [] } = useChannels()
  const [channelId, setChannelId] = useState('')
  const [importJobId, setImportJobId] = useState(null)
  const [syncResult, setSyncResult] = useState(null)
  const [connecting, setConnecting] = useState(false)

  const importExport = useImportExport()
  const triggerSync = useTriggerSync()
  const { job: importJob, status: importStatus, progress: importProgress } = useJobStatus(importJobId)

  // İçe aktarma bitince "Konuşmalar" listesini yenile — az önce ne kaydedildiğinin önizlemesi budur.
  useEffect(() => {
    if (importStatus === 'done') {
      queryClient.invalidateQueries({ queryKey: ['messenger-conversations'] })
    }
  }, [importStatus, queryClient])

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
    setImportJobId(null)
    importExport.mutate(
      { file, channelId: channelId || null },
      { onSuccess: (data) => setImportJobId(data.job_id) },
    )
  }

  function handleSync() {
    setSyncResult(null)
    triggerSync.mutate(undefined, { onSuccess: (data) => setSyncResult(data) })
  }

  let importResultSummary = null
  if (importJob?.result_ref) {
    try {
      importResultSummary = JSON.parse(importJob.result_ref)
    } catch {
      importResultSummary = null
    }
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
          Facebook "Bilgilerinizi İndirin" ile aldığın <code>message_1.json</code> dosyasını yükle
          (yalnızca mesajlar — CSV değil, JSON doğru format).
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

        {importJobId && (
          <div style={{ marginTop: 12 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <JobStatusBadge status={importStatus} />
              {importStatus && importStatus !== 'done' && importStatus !== 'error' && (
                <span style={{ fontSize: 12.5, color: 'var(--ink-2)' }}>%{importProgress}</span>
              )}
            </div>
            {importStatus === 'error' && (
              <p style={{ color: 'var(--critical)', fontSize: 13 }}>{importJob?.error_message}</p>
            )}
            {importResultSummary && (
              <div style={{ fontSize: 12.5, marginTop: 8 }}>
                <p style={{ color: 'var(--good)' }}>
                  {importResultSummary.processed} mesaj işlendi.
                </p>
                {importResultSummary.errors?.length > 0 && (
                  <ul style={{ color: 'var(--critical)' }}>
                    {importResultSummary.errors.map((err, i) => (
                      <li key={i}>{err}</li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 20 }}>
        Konuşmalar <span style={{ fontSize: 12.5, color: 'var(--ink-2)', fontWeight: 400 }}>
          (yüklenenin ne olarak kaydedildiğinin önizlemesi)
        </span>
      </h3>
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
