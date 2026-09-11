export function formatCurrency(value, currency = 'TRY') {
  return new Intl.NumberFormat('tr-TR', { style: 'currency', currency }).format(value)
}

export function formatDate(date) {
  return new Intl.DateTimeFormat('tr-TR').format(new Date(date))
}
