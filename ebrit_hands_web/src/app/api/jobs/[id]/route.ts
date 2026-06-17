import { NextResponse } from 'next/server'
import { ebritHandsClient } from '@/lib/ebrit-hands-client'
import { JobStatus } from '@/jobs/types'
import { logger } from '@/lib/logger'

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params
  logger.debug('job status request', { id })
  try {
    const data = await ebritHandsClient.getJobStatus(id)
    logger.debug('job status response', { id, data })
    return NextResponse.json(data)
  } catch (err) {
    logger.error('ebrit-hands unreachable', { id, err: String(err) })
    return NextResponse.json({ job_id: id, status: JobStatus.SUBMITTED }, { status: 503 })
  }
}
