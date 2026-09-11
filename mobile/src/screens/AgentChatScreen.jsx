import { askAgent, getAgentHistory } from '@satgit/api-client'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { FlatList, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native'

export default function AgentChatScreen() {
  const queryClient = useQueryClient()
  const { data: history = [] } = useQuery({ queryKey: ['agent-history'], queryFn: () => getAgentHistory() })
  const askMutation = useMutation({
    mutationFn: askAgent,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['agent-history'] }),
  })

  const [question, setQuestion] = useState('')

  function handleSend() {
    if (!question.trim()) return
    askMutation.mutate({ question }, { onSuccess: () => setQuestion('') })
  }

  const messages = [...history].reverse()

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Ajan</Text>

      <FlatList
        data={messages}
        keyExtractor={(item) => item.id}
        style={{ flex: 1 }}
        renderItem={({ item }) => (
          <View style={{ marginBottom: 12 }}>
            <View style={[styles.bubble, styles.userBubble]}>
              <Text style={styles.userText}>{item.question}</Text>
            </View>
            {item.answer && (
              <View style={[styles.bubble, styles.agentBubble]}>
                <Text style={styles.agentText}>{item.answer}</Text>
              </View>
            )}
          </View>
        )}
      />

      <View style={styles.form}>
        <TextInput
          style={styles.input}
          placeholder="Satışlarınla ilgili bir soru sor..."
          value={question}
          onChangeText={setQuestion}
        />
        <TouchableOpacity style={styles.button} onPress={handleSend} disabled={askMutation.isPending}>
          <Text style={styles.buttonText}>Gönder</Text>
        </TouchableOpacity>
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F1F4F1', padding: 16 },
  title: { fontSize: 26, fontWeight: '600', color: '#16232B', marginBottom: 12 },
  bubble: { maxWidth: '80%', borderRadius: 10, padding: 10 },
  userBubble: { backgroundColor: '#1F6F6B', alignSelf: 'flex-end' },
  agentBubble: { backgroundColor: '#E7ECE7', alignSelf: 'flex-start', marginTop: 6 },
  userText: { color: '#FFFFFF' },
  agentText: { color: '#16232B' },
  form: { flexDirection: 'row', gap: 8, marginTop: 12 },
  input: { flex: 1, borderWidth: 1, borderColor: '#C3CDC6', borderRadius: 6, padding: 10, backgroundColor: '#FFFFFF' },
  button: { backgroundColor: '#E08E1D', borderRadius: 6, paddingHorizontal: 16, justifyContent: 'center' },
  buttonText: { color: '#1A1206', fontWeight: '600' },
})
