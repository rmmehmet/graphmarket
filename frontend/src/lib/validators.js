export function isEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
}

export function isRequired(value) {
  return value !== null && value !== undefined && String(value).trim() !== ''
}
