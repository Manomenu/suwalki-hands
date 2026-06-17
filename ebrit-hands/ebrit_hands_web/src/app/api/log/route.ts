import { NextResponse } from 'next/server'
import { logger } from '@/lib/logger'

export async function POST(request: Request) {
  const { level, message, data } = await request.json()
  if (level === 'error') logger.error(message, data)
  else logger.info(message, data)
  return NextResponse.json({ ok: true })
}
