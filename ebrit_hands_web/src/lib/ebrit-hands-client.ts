import { JobStatus } from '@/jobs/types'

const BASE_URL = process.env.EBRIT_HANDS_URL ?? 'http://localhost:6009'

export const ebritHandsClient = {
  async listJobs(): Promise<unknown[]> {
    const res = await fetch(`${BASE_URL}/jobs/`, { cache: 'no-store' })
    if (!res.ok) return []
    return res.json()
  },

  async getJobStatus(id: string): Promise<{ job_id: string; status: JobStatus }> {
    const res = await fetch(`${BASE_URL}/jobs/${id}/status`, { cache: 'no-store' })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return res.json()
  },
}
