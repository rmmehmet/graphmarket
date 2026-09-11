import { useState } from 'react'
import { useChannels } from '../../hooks/useChannels'
import { useProducts } from '../../hooks/useProducts'
import { useCreateSale, useSales } from '../../hooks/useSales'
import { formatCurrency, formatDate } from '../../lib/formatters'
import SalesImport from './SalesImport'

export default function SalesHistory() {
  const { data: sales = [], isLoading } = useSales()
  const { data: products = [] } = useProducts()
  const { data: channels = [] } = useChannels()
  const createSale = useCreateSale()

  const [productId, setProductId] = useState('')
  const [channelId, setChannelId] = useState('')
  const [price, setPrice] = useState('')
  const [quantity, setQuantity] = useState('1')

  const productName = (id) => products.find((p) => p.id === id)?.name ?? '—'
  const channelName = (id) => channels.find((c) => c.id === id)?.name ?? '—'

  function handleSubmit(e) {
    e.preventDefault()
    createSale.mutate(
      {
        product_id: productId,
        channel_id: channelId,
        price: Number(price),
        quantity: Number(quantity),
      },
      { onSuccess: () => setPrice('') },
    )
  }

  return (
    <div>
      <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 26 }}>Satışlar</h2>

      <SalesImport />

      <form
        onSubmit={handleSubmit}
        style={{ display: 'flex', gap: 8, margin: '16px 0', flexWrap: 'wrap' }}
      >
        <select
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
          required
          style={inputStyle}
        >
          <option value="">Ürün seç</option>
          {products.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        <select
          value={channelId}
          onChange={(e) => setChannelId(e.target.value)}
          required
          style={inputStyle}
        >
          <option value="">Kanal seç</option>
          {channels.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
        <input
          placeholder="Fiyat"
          type="number"
          step="0.01"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
          style={{ ...inputStyle, width: 100 }}
        />
        <input
          placeholder="Adet"
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          required
          style={{ ...inputStyle, width: 80 }}
        />
        <button type="submit" disabled={createSale.isPending} style={buttonStyle}>
          Ekle
        </button>
      </form>

      {isLoading ? (
        <p>Yükleniyor...</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--line)' }}>
              <th style={thStyle}>Tarih</th>
              <th style={thStyle}>Ürün</th>
              <th style={thStyle}>Kanal</th>
              <th style={{ ...thStyle, textAlign: 'right' }}>Fiyat</th>
              <th style={{ ...thStyle, textAlign: 'right' }}>Adet</th>
            </tr>
          </thead>
          <tbody>
            {sales.map((s) => (
              <tr key={s.id} style={{ borderBottom: '1px solid var(--line)' }}>
                <td style={tdStyle}>{formatDate(s.sold_at)}</td>
                <td style={tdStyle}>{productName(s.product_id)}</td>
                <td style={tdStyle}>{channelName(s.channel_id)}</td>
                <td style={{ ...tdStyle, textAlign: 'right', fontFamily: 'var(--font-mono)' }}>
                  {formatCurrency(s.price)}
                </td>
                <td style={{ ...tdStyle, textAlign: 'right', fontFamily: 'var(--font-mono)' }}>
                  {s.quantity}
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

const thStyle = { textAlign: 'left', padding: '8px 4px', color: 'var(--ink-2)', fontSize: 12.5 }
const tdStyle = { padding: '8px 4px' }
