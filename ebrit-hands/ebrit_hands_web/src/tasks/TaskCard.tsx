'use client'
import type { Task } from './types'
import { JobStatus } from '@/jobs/types'
import JobCard from '@/jobs/JobCard'
import JobStatusDot from '@/jobs/JobStatusDot'
import { useJobPolling } from '@/jobs/useJobPolling'

interface Props {
  task: Task
  onRemove: (id: string) => void
  onStatusUpdate: (id: string, status: JobStatus) => void
}

export default function TaskCard({ task, onRemove, onStatusUpdate }: Props) {
  useJobPolling(task.jobId, task.status, onStatusUpdate)
  const isDone = task.status === JobStatus.FINISHED || task.status === JobStatus.ERROR
  const time = new Date(task.submittedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

  return (
    <JobCard status={task.status} onRemove={isDone ? () => onRemove(task.jobId) : undefined}>
      <span className="text-xs font-mono text-slate-400">{task.issueId}</span>
      <div>
        <p className="font-medium text-sm leading-snug">{task.title}</p>
        {task.description && (
          <p className="text-xs text-slate-500 mt-1 line-clamp-2">{task.description}</p>
        )}
      </div>
      <div className="flex items-center justify-between mt-auto pt-1 border-t border-slate-800">
        <JobStatusDot status={task.status} />
        <div className="text-xs text-slate-600">{task.sourceBranch} · {time}</div>
      </div>
    </JobCard>
  )
}
