import { NextResponse } from 'next/server'
import { logger } from '@/lib/logger'
import { ytracksChannelClient } from '@/lib/ytrack-channel-client'

export async function POST(request: Request) {
  const body = await request.json()
  logger.debug('submit request', { body })
  try {
    const { data, status } = await ytracksChannelClient.submitTask(body)
    logger.info('submit response', { status, data })
    return NextResponse.json(data, { status })
  } catch (err) {
    logger.error('ytrack-channel unreachable', { err: String(err) })
    return NextResponse.json({ error: 'ytrack-channel unreachable' }, { status: 503 })
  }
}
