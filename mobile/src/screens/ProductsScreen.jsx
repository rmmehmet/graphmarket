import { createProduct, listProducts } from '@satgit/api-client'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { FlatList, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native'

function formatCurrency(value) {
  return new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(value)
}

export default function ProductsScreen() {
  const queryClient = useQueryClient()
  const { data: products = [], isLoading } = useQuery({ queryKey: ['products'], queryFn: () => listProducts() })
  const createMutation = useMutation({
    mutationFn: createProduct,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['products'] }),
  })

  const [name, setName] = useState('')
  const [price, setPrice] = useState('')

  function handleAdd() {
    if (!name || !price) return
    createMutation.mutate(
      { name, category: null, base_price: Number(price) },
      { onSuccess: () => { setName(''); setPrice('') } },
    )
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Ürünler</Text>

      <View style={styles.form}>
        <TextInput style={styles.input} placeholder="Ürün adı" value={name} onChangeText={setName} />
        <TextInput
          style={[styles.input, { width: 90 }]}
          placeholder="Fiyat"
          keyboardType="numeric"
          value={price}
          onChangeText={setPrice}
        />
        <TouchableOpacity style={styles.button} onPress={handleAdd}>
          <Text style={styles.buttonText}>Ekle</Text>
        </TouchableOpacity>
      </View>

      {isLoading ? (
        <Text>Yükleniyor...</Text>
      ) : (
        <FlatList
          data={products}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <View style={styles.row}>
              <Text style={styles.rowName}>{item.name}</Text>
              <Text style={styles.rowPrice}>{formatCurrency(item.base_price)}</Text>
            </View>
          )}
        />
      )}
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F1F4F1', padding: 16 },
  title: { fontSize: 26, fontWeight: '600', color: '#16232B', marginBottom: 12 },
  form: { flexDirection: 'row', gap: 8, marginBottom: 16 },
  input: { flex: 1, borderWidth: 1, borderColor: '#C3CDC6', borderRadius: 6, padding: 10, backgroundColor: '#FFFFFF' },
  button: { backgroundColor: '#E08E1D', borderRadius: 6, paddingHorizontal: 16, justifyContent: 'center' },
  buttonText: { color: '#1A1206', fontWeight: '600' },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#DCE3DE',
  },
  rowName: { color: '#16232B' },
  rowPrice: { color: '#16232B', fontFamily: 'monospace' },
})
