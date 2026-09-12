import { useRef } from 'react'

// `directory`: true iken kullanıcı tek dosya yerine bir klasör seçer;
// onFileSelected o zaman tek File yerine File[] alır (klasördeki tüm dosyalar, recursive).
export default function FileUploadZone({
  onFileSelected,
  accept = '.csv',
  disabled,
  directory = false,
  label,
}) {
  const inputRef = useRef(null)

  function handleDrop(e) {
    e.preventDefault()
    if (directory) return // klasörleri drag&drop ile taramak ayrı bir API gerektirir, sadece tıkla-seç destekleniyor
    const file = e.dataTransfer.files?.[0]
    if (file) onFileSelected(file)
  }

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      onClick={() => inputRef.current?.click()}
      style={{
        border: '1px dashed var(--line-strong)',
        borderRadius: 'var(--r-md)',
        padding: 24,
        textAlign: 'center',
        color: 'var(--ink-2)',
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.6 : 1,
      }}
    >
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        multiple={directory}
        webkitdirectory={directory ? '' : undefined}
        directory={directory ? '' : undefined}
        hidden
        disabled={disabled}
        onChange={(e) => {
          const files = Array.from(e.target.files ?? [])
          if (!files.length) return
          onFileSelected(directory ? files : files[0])
          e.target.value = ''
        }}
      />
      {label ?? 'CSV dosyasını buraya sürükle veya seçmek için tıkla'}
    </div>
  )
}
