import { useState } from 'react'
import FileUploadZone from '../../components/ui/FileUploadZone'
import { useImportSales } from '../../hooks/useSales'

export default function SalesImport() {
  const importSales = useImportSales()
  const [result, setResult] = useState(null)

  function handleFile(file) {
    setResult(null)
    importSales.mutate(file, { onSuccess: (data) => setResult(data) })
  }

  return (
    <div style={{ marginBottom: 24 }}>
      <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 20 }}>CSV içe aktar</h3>
      <p style={{ fontSize: 12.5, color: 'var(--ink-2)' }}>
        Beklenen sütunlar: <code>product_name, channel_name, price, quantity, sold_at</code> (ürün/kanal
        adları mevcut kayıtlarla eşleşmeli)
      </p>
      <FileUploadZone onFileSelected={handleFile} disabled={importSales.isPending} />
      {importSales.isPending && <p>Yükleniyor...</p>}
      {result && (
        <div style={{ marginTop: 12, fontSize: 13 }}>
          <p style={{ color: 'var(--good)' }}>{result.imported_count} satış içe aktarıldı.</p>
          {result.errors.length > 0 && (
            <ul style={{ color: 'var(--critical)' }}>
              {result.errors.map((err, i) => (
                <li key={i}>{err}</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  )
}
