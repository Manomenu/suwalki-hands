'use client'
import { useRef, useState, useEffect } from 'react'
import type { Task } from './types'
import { JobStatus } from '@/jobs/types'

interface Repo { id: number; name: string }

interface Props {
  onSubmit: (task: Task) => void
  onCancel: () => void
}

export default function TaskForm({ onSubmit, onCancel }: Props) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [repos, setRepos] = useState<Repo[]>([])
  const [selectedRepoId, setSelectedRepoId] = useState(0)
  const issueIdRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    fetch('/api/repos')
      .then(r => r.json())
      .then((data: Repo[]) => {
        setRepos(data)
        if (data.length > 0) setSelectedRepoId(data[0].id)
      })
      .catch(() => {})
  }, [])

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setError('')
    const fd = new FormData(e.currentTarget)
    const data = Object.fromEntries(fd) as Record<string, string>

    setLoading(true)
    try {
      const res = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          issue_id: data.issueId,
          title: data.title,
          description: data.description,
          source_branch: data.sourceBranch || 'master',
          assignee_login: data.assigneeLogin || '',
          gitlab_project_id: selectedRepoId,
        }),
      })
      if (res.status === 502 || res.status === 503) {
        setError('ebrit-hands is unreachable — try again when the service is up.')
        return
      }
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const result = await res.json()
      onSubmit({
        jobId: result.job_id ?? '',
        issueId: data.issueId,
        title: data.title,
        description: data.description,
        sourceBranch: data.sourceBranch || 'master',
        assigneeLogin: data.assigneeLogin || '',
        gitlabProjectId: selectedRepoId,
        status: JobStatus.SUBMITTED,
        submittedAt: new Date().toISOString(),
      })
    } catch {
      setError('Failed to submit — is ytrack-channel running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6 w-full max-w-md shadow-2xl">
        <h2 className="text-lg font-semibold mb-5">New Task</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <div className="grid grid-cols-2 gap-3">
            <div className="flex flex-col gap-1">
              <label className="text-xs text-slate-400">Issue ID *</label>
              <input
                ref={issueIdRef}
                name="issueId"
                required
                autoFocus
                placeholder="SR-666"
                className="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm placeholder-slate-500 focus:outline-none focus:border-blue-500"
              />
            </div>
            <div className="flex flex-col gap-1">
              <label className="text-xs text-slate-400">Source Branch</label>
              <input
                name="sourceBranch"
                placeholder="master"
                className="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm placeholder-slate-500 focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          {repos.length > 1 && (
            <div className="flex flex-col gap-1">
              <label className="text-xs text-slate-400">Repository</label>
              <select
                value={selectedRepoId}
                onChange={e => setSelectedRepoId(Number(e.target.value))}
                className="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
              >
                {repos.map(r => (
                  <option key={r.id} value={r.id}>{r.name}</option>
                ))}
              </select>
            </div>
          )}

          <div className="flex flex-col gap-1">
            <label className="text-xs text-slate-400">Title *</label>
            <input
              name="title"
              required
              placeholder="Add README"
              className="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs text-slate-400">Assignee Login</label>
            <input
              name="assigneeLogin"
              placeholder="ebrit-hands"
              className="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs text-slate-400">Description</label>
            <textarea
              name="description"
              rows={3}
              placeholder="Describe the task..."
              className="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm placeholder-slate-500 focus:outline-none focus:border-blue-500 resize-none"
            />
          </div>

          {error && <p className="text-red-400 text-xs">{error}</p>}

          <div className="flex gap-2 justify-end pt-1">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 text-sm text-slate-400 hover:text-white rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              {loading ? 'Submitting…' : 'Submit Task →'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
