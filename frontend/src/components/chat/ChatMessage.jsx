import CitationList from './CitationList'

export default function ChatMessage({ role, text, citations }) {
  const isUser = role === 'user'

  return (
    <div style={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', marginBottom: 10 }}>
      <div
        style={{
          maxWidth: '70%',
          padding: '10px 14px',
          borderRadius: 'var(--r-md)',
          background: isUser ? 'var(--teal)' : 'var(--surface-2)',
          color: isUser ? '#fff' : 'var(--ink)',
          whiteSpace: 'pre-wrap',
        }}
      >
        {text}
        {!isUser && <CitationList citations={citations} />}
      </div>
    </div>
  )
}
