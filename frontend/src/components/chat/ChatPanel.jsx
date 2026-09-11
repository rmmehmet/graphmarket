import { useState } from 'react'
import ChatMessage from './ChatMessage'

export default function ChatPanel({ messages, onSend, sending }) {
  const [input, setInput] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    if (!input.trim()) return
    onSend(input)
    setInput('')
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div style={{ flex: 1, overflowY: 'auto', padding: 4 }}>
        {messages.map((m, i) => (
          <ChatMessage key={i} role={m.role} text={m.text} citations={m.citations} />
        ))}
      </div>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8, marginTop: 12 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Satışlarınla ilgili bir soru sor..."
          style={{
            flex: 1,
            padding: '9px 12px',
            borderRadius: 'var(--r-sm)',
            border: '1px solid var(--line-strong)',
          }}
        />
        <button
          type="submit"
          disabled={sending}
          style={{
            padding: '9px 18px',
            borderRadius: 'var(--r-sm)',
            border: 'none',
            background: 'var(--accent)',
            color: 'var(--on-accent)',
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          Gönder
        </button>
      </form>
    </div>
  )
}
