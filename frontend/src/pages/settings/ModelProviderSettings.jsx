import { useState } from 'react'
import UsageMeter from '../../components/ui/UsageMeter'
import { useModelProfiles, useTestModelProfile, useUpdateModelProfile } from '../../hooks/useModelProfiles'
import { useUsage } from '../../hooks/useUsage'

const NODE_LABELS = {
  planner: 'Planlayıcı',
  extraction: 'Çıkarım',
  synthesis: 'Sentez',
  verification: 'Doğrulama',
}

const PROVIDER_OPTIONS = [
  { value: 'ollama', label: 'Ollama (yerel)' },
  { value: 'huggingface', label: 'Hugging Face' },
  { value: 'anthropic_api', label: 'Anthropic API' },
  { value: 'claude_subscription', label: 'Claude Code (abonelik)' },
]

export default function ModelProviderSettings() {
  const { data: profiles = [], isLoading } = useModelProfiles()
  const { data: usage } = useUsage()

  return (
    <div>
      <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 26 }}>Model Sağlayıcı Ayarları</h2>

      <div style={{ marginBottom: 16 }}>
        <UsageMeter usage={usage} />
      </div>

      {isLoading ? (
        <p>Yükleniyor...</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 16 }}>
          {profiles.map((profile) => (
            <ProfileRow key={profile.node} profile={profile} />
          ))}
        </div>
      )}
    </div>
  )
}

function ProfileRow({ profile }) {
  const [provider, setProvider] = useState(profile.provider)
  const [modelName, setModelName] = useState(profile.model_name ?? '')
  const [apiKey, setApiKey] = useState('')
  const [testResult, setTestResult] = useState(null)

  const updateProfile = useUpdateModelProfile()
  const testProfile = useTestModelProfile()

  function handleSave() {
    updateProfile.mutate(
      { node: profile.node, provider, model_name: modelName || null, api_key: apiKey || null },
      { onSuccess: () => setApiKey('') },
    )
  }

  function handleTest() {
    setTestResult(null)
    testProfile.mutate(profile.node, { onSuccess: (data) => setTestResult(data) })
  }

  return (
    <div
      style={{
        background: 'var(--surface)',
        border: '1px solid var(--line)',
        borderRadius: 'var(--r-md)',
        padding: 16,
      }}
    >
      <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 18, marginTop: 0 }}>
        {NODE_LABELS[profile.node] ?? profile.node}
      </h3>

      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center' }}>
        <select value={provider} onChange={(e) => setProvider(e.target.value)} style={inputStyle}>
          {PROVIDER_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        <input
          placeholder="Model adı"
          value={modelName}
          onChange={(e) => setModelName(e.target.value)}
          style={inputStyle}
        />
        <input
          placeholder={profile.has_api_key ? 'API anahtarı (kayıtlı — değiştirmek için gir)' : 'API anahtarı'}
          type="password"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          style={{ ...inputStyle, width: 260 }}
        />
        <button onClick={handleSave} disabled={updateProfile.isPending} style={buttonStyle}>
          Kaydet
        </button>
        <button onClick={handleTest} disabled={testProfile.isPending} style={ghostButtonStyle}>
          Bağlantıyı test et
        </button>
      </div>

      {testResult && (
        <p style={{ fontSize: 12.5, marginTop: 8, color: testResult.ok ? 'var(--good)' : 'var(--critical)' }}>
          {testResult.ok
            ? `Bağlantı başarılı (${testResult.latency_ms}ms)`
            : `Başarısız: ${testResult.error}`}
        </p>
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
  padding: '9px 18px',
  borderRadius: 'var(--r-sm)',
  border: '1px solid var(--teal)',
  background: 'transparent',
  color: 'var(--teal)',
  cursor: 'pointer',
}
