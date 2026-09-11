import { useRef } from 'react'

export default function FileUploadZone({ onFileSelected, accept = '.csv', disabled }) {
  const inputRef = useRef(null)

  function handleDrop(e) {
    e.preventDefault()
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
        hidden
        disabled={disabled}
        onChange={(e) => {
          const file = e.target.files?.[0]
          if (file) onFileSelected(file)
          e.target.value = ''
        }}
      />
      CSV dosyasını buraya sürükle veya seçmek için tıkla
    </div>
  )
}
