import fs from 'fs'
import path from 'path'

const LOGS_DIR = process.env.LOGS_DIR ?? path.join(process.cwd(), '..', 'logs')

try { fs.mkdirSync(LOGS_DIR, { recursive: true }) } catch { /* ignore */ }
const SERVICE = 'web'
const RETENTION_DAYS = 7

function today(): string {
  return new Date().toISOString().slice(0, 10)
}

function purgeOldLogs() {
  const cutoff = Date.now() - RETENTION_DAYS * 24 * 60 * 60 * 1000
  for (const dir of [LOGS_DIR, path.join(LOGS_DIR, 'archive')]) {
    try {
      for (const f of fs.readdirSync(dir)) {
        if (!f.endsWith('.log')) continue
        const full = path.join(dir, f)
        if (fs.statSync(full).mtimeMs < cutoff) fs.unlinkSync(full)
      }
    } catch { /* ignore */ }
  }
}

let lastArchivedDate = ''

function archiveOldLogs() {
  const todayStr = today()
  if (lastArchivedDate === todayStr) return
  lastArchivedDate = todayStr
  try {
    const archiveDir = path.join(LOGS_DIR, 'archive')
    fs.mkdirSync(archiveDir, { recursive: true })
    for (const f of fs.readdirSync(LOGS_DIR)) {
      if (!f.endsWith('.log')) continue
      if (f.startsWith(todayStr)) continue
      fs.renameSync(path.join(LOGS_DIR, f), path.join(archiveDir, f))
    }
  } catch { /* ignore */ }
  purgeOldLogs()
}

function write(file: string, level: string, message: string, data?: unknown) {
  archiveOldLogs()
  const line =
    `${new Date().toISOString()} ${level.padEnd(5)} ${message}` +
    (data !== undefined ? ' ' + JSON.stringify(data) : '') +
    '\n'
  try {
    fs.appendFileSync(path.join(LOGS_DIR, file), line)
  } catch {
    // logs dir not mounted — ignore
  }
}

function logFile() {
  return `${today()}.${SERVICE}.log`
}

function debugFile() {
  return `debug.${today()}.${SERVICE}.log`
}

export const logger = {
  info: (message: string, data?: unknown) => {
    write(logFile(), 'INFO', message, data)
    write(debugFile(), 'INFO', message, data)
  },
  error: (message: string, data?: unknown) => {
    write(logFile(), 'ERROR', message, data)
    write(debugFile(), 'ERROR', message, data)
  },
  debug: (message: string, data?: unknown) => {
    write(debugFile(), 'DEBUG', message, data)
  },
}
