import PriceTrendChart from '../components/charts/PriceTrendChart'
import StatCard from '../components/ui/StatCard'
import UsageMeter from '../components/ui/UsageMeter'
import { useSales, useSalesAnalytics } from '../hooks/useSales'
import { useProducts } from '../hooks/useProducts'
import { useChannels } from '../hooks/useChannels'
import { useUsage } from '../hooks/useUsage'
import { formatCurrency, formatDate } from '../lib/formatters'

export default function Dashboard() {
  const { data: analytics, isLoading: analyticsLoading } = useSalesAnalytics('week')
  const { data: recentSales = [], isLoading: salesLoading } = useSales()
  const { data: products = [] } = useProducts()
  const { data: channels = [] } = useChannels()
  const { data: usage } = useUsage()

  const productName = (id) => products.find((p) => p.id === id)?.name ?? '—'
  const channelName = (id) => channels.find((c) => c.id === id)?.name ?? '—'

  return (
    <div>
      <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 26 }}>Panel</h2>

      <div style={{ display: 'flex', gap: 12, margin: '16px 0', flexWrap: 'wrap' }}>
        <StatCard
          label="Toplam gelir"
          value={analyticsLoading ? '—' : formatCurrency(analytics?.totals.revenue ?? 0)}
        />
        <StatCard label="Satılan adet" value={analyticsLoading ? '—' : analytics?.totals.quantity ?? 0} />
        <StatCard label="Ürün sayısı" value={products.length} />
        <StatCard label="Kanal sayısı" value={channels.length} />
      </div>

      <div style={{ marginBottom: 24 }}>
        <UsageMeter usage={usage} />
      </div>

      <div
        style={{
          background: 'var(--surface)',
          border: '1px solid var(--line)',
          borderRadius: 'var(--r-md)',
          padding: 16,
          marginBottom: 24,
        }}
      >
        <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 20, marginTop: 0 }}>
          Haftalık gelir trendi
        </h3>
        {analyticsLoading ? <p>Yükleniyor...</p> : <PriceTrendChart series={analytics?.series} />}
      </div>

      <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 20 }}>Son satışlar</h3>
      {salesLoading ? (
        <p>Yükleniyor...</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--line)' }}>
              <th style={thStyle}>Tarih</th>
              <th style={thStyle}>Ürün</th>
              <th style={thStyle}>Kanal</th>
              <th style={{ ...thStyle, textAlign: 'right' }}>Tutar</th>
            </tr>
          </thead>
          <tbody>
            {recentSales.slice(0, 8).map((s) => (
              <tr key={s.id} style={{ borderBottom: '1px solid var(--line)' }}>
                <td style={tdStyle}>{formatDate(s.sold_at)}</td>
                <td style={tdStyle}>{productName(s.product_id)}</td>
                <td style={tdStyle}>{channelName(s.channel_id)}</td>
                <td style={{ ...tdStyle, textAlign: 'right', fontFamily: 'var(--font-mono)' }}>
                  {formatCurrency(s.price * s.quantity)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

const thStyle = { textAlign: 'left', padding: '8px 4px', color: 'var(--ink-2)', fontSize: 12.5 }
const tdStyle = { padding: '8px 4px' }
