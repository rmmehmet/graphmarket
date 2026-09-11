import * as Sentry from '@sentry/react'

function Fallback({ error, resetError }) {
  return (
    <div
      style={{
        maxWidth: 480,
        margin: '80px auto',
        padding: 24,
        textAlign: 'center',
        fontFamily: 'var(--font-body)',
      }}
    >
      <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 26 }}>Bir şeyler ters gitti</h1>
      <p style={{ color: 'var(--ink-2)', fontSize: 14 }}>
        Beklenmeyen bir hata oluştu. Sayfayı yenilemeyi deneyebilirsin.
      </p>
      {import.meta.env.DEV && (
        <pre style={{ textAlign: 'left', fontSize: 12, color: 'var(--critical)', overflow: 'auto' }}>
          {error?.message}
        </pre>
      )}
      <button
        onClick={resetError}
        style={{
          marginTop: 16,
          padding: '9px 18px',
          borderRadius: 'var(--r-sm)',
          border: 'none',
          background: 'var(--accent)',
          color: 'var(--on-accent)',
          fontWeight: 600,
          cursor: 'pointer',
        }}
      >
        Tekrar dene
      </button>
    </div>
  )
}

export default function ErrorBoundary({ children }) {
  return <Sentry.ErrorBoundary fallback={Fallback}>{children}</Sentry.ErrorBoundary>
}
