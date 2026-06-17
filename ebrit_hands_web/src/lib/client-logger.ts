function send(level: 'info' | 'error', message: string, data?: unknown) {
  fetch('/api/log', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ level, message, data }),
  }).catch(() => {})
}

export const clientLogger = {
  info:  (message: string, data?: unknown) => send('info',  message, data),
  error: (message: string, data?: unknown) => send('error', message, data),
}
