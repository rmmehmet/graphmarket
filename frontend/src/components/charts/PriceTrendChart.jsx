import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

export default function PriceTrendChart({ series }) {
  if (!series?.length) {
    return <p style={{ color: 'var(--ink-2)' }}>Henüz veri yok.</p>
  }

  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={series}>
        <CartesianGrid stroke="var(--line)" vertical={false} />
        <XAxis dataKey="label" tick={{ fontSize: 12 }} stroke="var(--ink-2)" />
        <YAxis tick={{ fontSize: 12 }} stroke="var(--ink-2)" />
        <Tooltip />
        <Line type="monotone" dataKey="revenue" stroke="var(--teal)" strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  )
}
