import { JobStatus } from './types'
import { STATUS_CONFIG } from './JobStatusDot'

interface Props {
  status: JobStatus
  onRemove?: () => void
  children: React.ReactNode
}

export default function JobCard({ status, onRemove, children }: Props) {
  const { ring } = STATUS_CONFIG[status] ?? STATUS_CONFIG[JobStatus.SUBMITTED]
  return (
    <div className={`bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col gap-3 group relative ${ring}`}>
      {onRemove && (
        <button
          onClick={onRemove}
          className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 text-slate-600 hover:text-slate-300 text-lg leading-none transition-opacity"
          aria-label="Remove"
        >
          ×
        </button>
      )}
      {children}
    </div>
  )
}
