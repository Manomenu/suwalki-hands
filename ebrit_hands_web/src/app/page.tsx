'use client'
import { useEffect, useState, useCallback } from 'react'
import TaskCard from '@/tasks/TaskCard'
import TaskForm from '@/tasks/TaskForm'
import type { Task } from '@/tasks/types'
import { JobStatus, JobType, type Job } from '@/jobs/types'
import ReviewCard from '@/reviews/ReviewCard'
import DiscoveredJobCard from '@/jobs/DiscoveredJobCard'
import { clientLogger } from '@/lib/client-logger'

const STORAGE_KEY = 'ebrit-tasks'
const DISMISSED_KEY = 'ebrit-dismissed-jobs'

export default function Home() {
  const [localTasks, setLocalTasks] = useState<Task[]>([])
  const [apiJobs, setApiJobs] = useState<Job[]>([])
  const [discoveredAt, setDiscoveredAt] = useState<Record<string, string>>({})
  const [dismissedJobIds, setDismissedJobIds] = useState<Set<string>>(new Set())
  const [showForm, setShowForm] = useState(false)

  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      if (saved) setLocalTasks(JSON.parse(saved))
    } catch { /* ignore */ }
    try {
      const saved = localStorage.getItem(DISMISSED_KEY)
      if (saved) setDismissedJobIds(new Set(JSON.parse(saved)))
    } catch { /* ignore */ }
  }, [])

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(localTasks))
  }, [localTasks])

  useEffect(() => {
    localStorage.setItem(DISMISSED_KEY, JSON.stringify([...dismissedJobIds]))
  }, [dismissedJobIds])

  useEffect(() => {
    async function poll() {
      try {
        const res = await fetch('/api/jobs', { cache: 'no-store' })
        if (!res.ok) return
        const data: Array<{ job_id: string; status: string; job_type: string; identifier: string }> = await res.json()
        setApiJobs(data.map(j => ({
          jobId: j.job_id,
          status: j.status as JobStatus,
          jobType: j.job_type as JobType,
          identifier: j.identifier,
        })))
      } catch { /* ignore */ }
    }
    poll()
    const id = setInterval(poll, 3000)
    return () => clearInterval(id)
  }, [])

  // track first appearance time for each discovered job
  useEffect(() => {
    if (apiJobs.length === 0) return
    const now = new Date().toISOString()
    setDiscoveredAt(prev => {
      let changed = false
      const next = { ...prev }
      for (const job of apiJobs) {
        if (!next[job.jobId]) {
          next[job.jobId] = now
          changed = true
        }
      }
      return changed ? next : prev
    })
  }, [apiJobs])

  const addTask = useCallback((task: Task) => {
    setLocalTasks(prev => [task, ...prev])
    setShowForm(false)
  }, [])

  const removeTask = useCallback((id: string) => {
    setLocalTasks(prev => {
      const task = prev.find(t => t.jobId === id)
      if (task) clientLogger.info('task removed', { jobId: id, issueId: task.issueId, status: task.status })
      return prev.filter(t => t.jobId !== id)
    })
    setDismissedJobIds(prev => new Set([...prev, id]))
  }, [])

  const updateStatus = useCallback((id: string, status: JobStatus) => {
    setLocalTasks(prev => prev.map(t => {
      if (t.jobId !== id) return t
      if (t.status !== status) clientLogger.info('task status changed', { jobId: id, issueId: t.issueId, from: t.status, to: status })
      return { ...t, status }
    }))
  }, [])

  const updateApiJobStatus = useCallback((id: string, status: JobStatus) => {
    setApiJobs(prev => prev.map(j => {
      if (j.jobId !== id) return j
      if (j.status !== status) clientLogger.info('job status changed', { jobId: id, identifier: j.identifier, jobType: j.jobType, from: j.status, to: status })
      return { ...j, status }
    }))
  }, [])

  const dismissJob = useCallback((id: string) => {
    setApiJobs(prev => {
      const job = prev.find(j => j.jobId === id)
      if (job) clientLogger.info('job dismissed', { jobId: id, identifier: job.identifier, jobType: job.jobType, status: job.status })
      return prev
    })
    setDismissedJobIds(prev => new Set([...prev, id]))
  }, [])

  const tasksByJobId = new Map(localTasks.map(t => [t.jobId, t]))
  const apiJobIds = new Set(apiJobs.map(j => j.jobId))
  const pendingTasks = localTasks.filter(t => !apiJobIds.has(t.jobId))
  const visibleApiJobs = apiJobs.filter(j => !dismissedJobIds.has(j.jobId))
  const totalCount = pendingTasks.length + visibleApiJobs.length

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-slate-800 px-6 py-4 flex items-center justify-between sticky top-0 bg-slate-950/80 backdrop-blur z-10">
        <div>
          <h1 className="text-base font-semibold tracking-tight">ebrit-hands</h1>
          <p className="text-xs text-slate-500">{totalCount} job{totalCount !== 1 ? 's' : ''}</p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-1.5 transition-colors"
        >
          <span className="text-base leading-none">+</span> New Task
        </button>
      </header>

      <main className="flex-1 p-6">
        {totalCount === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-slate-600">
            <p className="text-lg mb-1">No jobs yet</p>
            <p className="text-sm">Click <span className="text-slate-400">+ New Task</span> to get started</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {pendingTasks.map(task => (
              <TaskCard key={task.jobId} task={task} onRemove={removeTask} onStatusUpdate={updateStatus} />
            ))}
            {visibleApiJobs.map(job => {
              const localTask = tasksByJobId.get(job.jobId)
              if (localTask) {
                return <TaskCard key={job.jobId} task={localTask} onRemove={removeTask} onStatusUpdate={updateStatus} />
              }
              if (job.jobType === JobType.REVIEW) {
                return (
                  <ReviewCard
                    key={job.jobId}
                    job={job}
                    discoveredAt={discoveredAt[job.jobId] ?? new Date().toISOString()}
                    onStatusUpdate={updateApiJobStatus}
                    onRemove={dismissJob}
                  />
                )
              }
              return (
                <DiscoveredJobCard
                  key={job.jobId}
                  job={job}
                  onStatusUpdate={updateApiJobStatus}
                  onRemove={dismissJob}
                />
              )
            })}
          </div>
        )}
      </main>

      {showForm && <TaskForm onSubmit={addTask} onCancel={() => setShowForm(false)} />}
    </div>
  )
}
