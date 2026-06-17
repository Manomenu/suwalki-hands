import { useEffect, useRef } from 'react'
import { JobStatus } from './types'

const POLL_INTERVAL = 2000
const FAILURE_THRESHOLD = 3

export function useJobPolling(
  jobId: string,
  currentStatus: JobStatus,
  onStatusUpdate: (id: string, status: JobStatus) => void,
) {
  const statusRef = useRef(currentStatus)
  const onUpdateRef = useRef(onStatusUpdate)
  statusRef.current = currentStatus
  onUpdateRef.current = onStatusUpdate

  useEffect(() => {
    const failures = { count: 0 }

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`/api/jobs/${jobId}`)
        if (res.ok) {
          failures.count = 0
          const data = await res.json()
          if (data.status && data.status !== statusRef.current) {
            onUpdateRef.current(jobId, data.status as JobStatus)
          }
        } else {
          if (++failures.count === FAILURE_THRESHOLD) {
            onUpdateRef.current(jobId, JobStatus.ERROR)
          }
        }
      } catch {
        if (++failures.count === FAILURE_THRESHOLD) {
          onUpdateRef.current(jobId, JobStatus.ERROR)
        }
      }
    }, POLL_INTERVAL)

    return () => clearInterval(interval)
  }, [jobId])
}
