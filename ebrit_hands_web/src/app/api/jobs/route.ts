import { NextResponse } from 'next/server'
import { ebritHandsClient } from '@/lib/ebrit-hands-client'

export async function GET() {
  return NextResponse.json(await ebritHandsClient.listJobs())
}
