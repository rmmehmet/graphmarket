import { useMemo, useState } from 'react'
import ChatPanel from '../../components/chat/ChatPanel'
import { useAgentHistory, useAskAgent } from '../../hooks/useAgentChat'

export default function AgentChat() {
  const { data: history = [] } = useAgentHistory()
  const askAgent = useAskAgent()
  const [pending, setPending] = useState([])

  const messages = useMemo(() => {
    const fromHistory = [...history].reverse().flatMap((h) => {
      const items = [{ role: 'user', text: h.question }]
      if (h.answer) items.push({ role: 'agent', text: h.answer, citations: h.citations })
      return items
    })
    return [...fromHistory, ...pending]
  }, [history, pending])

  function handleSend(question) {
    setPending((prev) => [...prev, { role: 'user', text: question }])
    askAgent.mutate(
      { question },
      {
        onSuccess: (data) => {
          setPending((prev) => [...prev, { role: 'agent', text: data.answer, citations: data.citations }])
        },
        onError: () => {
          setPending((prev) => [
            ...prev,
            { role: 'agent', text: 'Bir hata oluştu, tekrar dener misin?' },
          ])
        },
      },
    )
  }

  return (
    <div style={{ height: 'calc(100vh - 56px - 48px)', display: 'flex', flexDirection: 'column' }}>
      <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 26 }}>Ajan</h2>
      <div style={{ flex: 1 }}>
        <ChatPanel messages={messages} onSend={handleSend} sending={askAgent.isPending} />
      </div>
    </div>
  )
}
