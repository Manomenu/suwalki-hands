export { JobStatus as TaskStatus } from '@/jobs/types'
import { JobStatus } from '@/jobs/types'

export interface Task {
  jobId: string
  issueId: string
  title: string
  description: string
  sourceBranch: string
  assigneeLogin: string
  gitlabProjectId: number
  status: JobStatus
  submittedAt: string
}
