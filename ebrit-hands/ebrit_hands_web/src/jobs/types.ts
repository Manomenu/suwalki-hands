export enum JobStatus {
  SUBMITTED = 'submitted',
  IN_PROGRESS = 'in_progress',
  FINISHED = 'finished',
  ERROR = 'error',
}

export enum JobType {
  TASK = 'task',
  REVIEW = 'review',
}

export interface Job {
  jobId: string
  status: JobStatus
  jobType: JobType
  identifier: string
}
