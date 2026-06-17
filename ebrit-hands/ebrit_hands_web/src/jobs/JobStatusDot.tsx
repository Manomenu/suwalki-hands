import { JobStatus } from './types'

export const STATUS_CONFIG: Record<JobStatus, { dot: string; label: string; ring: string }> = {
  [JobStatus.SUBMITTED]:   { dot: 'bg-slate-400',               label: 'Submitted',   ring: '' },
  [JobStatus.IN_PROGRESS]: { dot: 'bg-amber-400 animate-pulse', label: 'In Progress', ring: 'ring-1 ring-amber-500/30' },
  [JobStatus.FINISHED]:    { dot: 'bg-green-400',               label: 'Finished',    ring: 'ring-1 ring-green-500/30' },
  [JobStatus.ERROR]:       { dot: 'bg-red-400',                 label: 'Error',       ring: 'ring-1 ring-red-500/30' },
}

export default function JobStatusDot({ status }: { status: JobStatus }) {
  const cfg = STATUS_CONFIG[status] ?? STATUS_CONFIG.submitted
  return (
    <div className="flex items-center gap-2">
      <span className={`w-2 h-2 rounded-full ${cfg.dot}`} />
      <span className="text-xs text-slate-400">{cfg.label}</span>
    </div>
  )
}
