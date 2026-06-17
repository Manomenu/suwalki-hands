'use client'
import { JobStatus, type Job } from '@/jobs/types'
import JobCard from '@/jobs/JobCard'
import JobStatusDot from '@/jobs/JobStatusDot'
import { useJobPolling } from '@/jobs/useJobPolling'

interface Props {
  job: Job
  discoveredAt: string
  onStatusUpdate: (id: string, status: JobStatus) => void
  onRemove: (id: string) => void
}

export default function ReviewCard({ job, discoveredAt, onStatusUpdate, onRemove }: Props) {
  useJobPolling(job.jobId, job.status, onStatusUpdate)
  const isDone = job.status === JobStatus.FINISHED || job.status === JobStatus.ERROR
  const time = new Date(discoveredAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

  return (
    <JobCard status={job.status} onRemove={isDone ? () => onRemove(job.jobId) : undefined}>
      <div>
        <span className="text-xs text-slate-500 uppercase tracking-wide">Review</span>
        <p className="font-medium text-sm mt-0.5 leading-snug">{job.identifier}</p>
      </div>
      <div className="flex items-center justify-between mt-auto pt-1 border-t border-slate-800">
        <JobStatusDot status={job.status} />
        <span className="text-xs text-slate-600">{time}</span>
      </div>
    </JobCard>
  )
}
