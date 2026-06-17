'use client'
import { JobStatus, type Job } from './types'
import JobCard from './JobCard'
import JobStatusDot from './JobStatusDot'
import { useJobPolling } from './useJobPolling'

interface Props {
  job: Job
  onStatusUpdate: (id: string, status: JobStatus) => void
  onRemove: (id: string) => void
}

export default function DiscoveredJobCard({ job, onStatusUpdate, onRemove }: Props) {
  useJobPolling(job.jobId, job.status, onStatusUpdate)
  const isDone = job.status === JobStatus.FINISHED || job.status === JobStatus.ERROR

  return (
    <JobCard status={job.status} onRemove={isDone ? () => onRemove(job.jobId) : undefined}>
      <span className="text-xs font-mono text-slate-400">{job.identifier}</span>
      <div className="mt-auto pt-1 border-t border-slate-800">
        <JobStatusDot status={job.status} />
      </div>
    </JobCard>
  )
}
