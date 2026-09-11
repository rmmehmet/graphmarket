import { useState } from 'react'
import { useCreateProduct, useDeleteProduct, useProducts } from '../../hooks/useProducts'
import { formatCurrency } from '../../lib/formatters'

export default function ProductList() {
  const { data: products = [], isLoading } = useProducts()
  const createProduct = useCreateProduct()
  const deleteProduct = useDeleteProduct()

  const [name, setName] = useState('')
  const [category, setCategory] = useState('')
  const [basePrice, setBasePrice] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    createProduct.mutate(
      { name, category: category || null, base_price: Number(basePrice) },
      {
        onSuccess: () => {
          setName('')
          setCategory('')
          setBasePrice('')
        },
      },
    )
  }

  return (
    <div>
      <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 26 }}>Ürünler</h2>

      <form
        onSubmit={handleSubmit}
        style={{ display: 'flex', gap: 8, margin: '16px 0', flexWrap: 'wrap' }}
      >
        <input
          placeholder="Ürün adı"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={inputStyle}
        />
        <input
          placeholder="Kategori"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          style={inputStyle}
        />
        <input
          placeholder="Fiyat"
          type="number"
          step="0.01"
          value={basePrice}
          onChange={(e) => setBasePrice(e.target.value)}
          required
          style={{ ...inputStyle, width: 120 }}
        />
        <button type="submit" disabled={createProduct.isPending} style={buttonStyle}>
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
              <th style={thStyle}>Kategori</th>
              <th style={{ ...thStyle, textAlign: 'right' }}>Fiyat</th>
              <th style={thStyle} />
            </tr>
          </thead>
          <tbody>
            {products.map((p) => (
              <tr key={p.id} style={{ borderBottom: '1px solid var(--line)' }}>
                <td style={tdStyle}>{p.name}</td>
                <td style={tdStyle}>{p.category ?? '—'}</td>
                <td style={{ ...tdStyle, textAlign: 'right', fontFamily: 'var(--font-mono)' }}>
                  {formatCurrency(p.base_price)}
                </td>
                <td style={tdStyle}>
                  <button onClick={() => deleteProduct.mutate(p.id)} style={ghostButtonStyle}>
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
