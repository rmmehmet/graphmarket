import { getSalesAnalytics, getUsage } from '@satgit/api-client'
import { useQuery } from '@tanstack/react-query'
import { ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native'
import { authStore } from '../authStore'

function formatCurrency(value) {
  return new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(value)
}

export default function DashboardScreen({ navigation }) {
  const { data: analytics, isLoading } = useQuery({
    queryKey: ['sales-analytics', 'week'],
    queryFn: () => getSalesAnalytics('week'),
  })
  const { data: usage } = useQuery({ queryKey: ['usage'], queryFn: getUsage })

  return (
    <ScrollView style={styles.container} contentContainerStyle={{ padding: 16 }}>
      <View style={styles.headerRow}>
        <Text style={styles.title}>Panel</Text>
        <TouchableOpacity onPress={authStore.clearTokens}>
          <Text style={styles.logout}>Çıkış yap</Text>
        </TouchableOpacity>
      </View>

      {isLoading ? (
        <Text>Yükleniyor...</Text>
      ) : (
        <View style={styles.statsRow}>
          <View style={styles.statCard}>
            <Text style={styles.statLabel}>TOPLAM GELİR</Text>
            <Text style={styles.statValue}>{formatCurrency(analytics?.totals.revenue ?? 0)}</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statLabel}>SATILAN ADET</Text>
            <Text style={styles.statValue}>{analytics?.totals.quantity ?? 0}</Text>
          </View>
        </View>
      )}

      {usage && (
        <View style={styles.usageCard}>
          <Text style={styles.usageTitle}>
            Kullanım — {usage.plan} plan ({usage.period})
          </Text>
          {usage.breakdown.map((item) => (
            <Text key={item.job_type} style={styles.usageRow}>
              {item.job_type}: {item.used}
              {item.limit !== null ? ` / ${item.limit}` : ' · sınırsız'}
            </Text>
          ))}
        </View>
      )}

      <View style={styles.navRow}>
        <TouchableOpacity style={styles.navButton} onPress={() => navigation.navigate('Products')}>
          <Text style={styles.navButtonText}>Ürünler</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navButton} onPress={() => navigation.navigate('AgentChat')}>
          <Text style={styles.navButtonText}>Ajan</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F1F4F1' },
  headerRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 },
  title: { fontSize: 26, fontWeight: '600', color: '#16232B' },
  logout: { color: '#4B5D63' },
  statsRow: { flexDirection: 'row', gap: 12, marginBottom: 16 },
  statCard: { flex: 1, backgroundColor: '#FFFFFF', borderRadius: 10, borderWidth: 1, borderColor: '#DCE3DE', padding: 16 },
  statLabel: { fontSize: 11, color: '#4B5D63', marginBottom: 4 },
  statValue: { fontSize: 20, fontWeight: '600', color: '#16232B' },
  usageCard: { backgroundColor: '#FFFFFF', borderRadius: 10, borderWidth: 1, borderColor: '#DCE3DE', padding: 16 },
  usageTitle: { fontSize: 12, color: '#4B5D63', marginBottom: 8, textTransform: 'uppercase' },
  usageRow: { fontSize: 13, color: '#16232B', marginBottom: 4 },
  navRow: { flexDirection: 'row', gap: 12, marginTop: 16 },
  navButton: { flex: 1, backgroundColor: '#FFFFFF', borderWidth: 1, borderColor: '#1F6F6B', borderRadius: 6, padding: 12, alignItems: 'center' },
  navButtonText: { color: '#1F6F6B', fontWeight: '600' },
})
