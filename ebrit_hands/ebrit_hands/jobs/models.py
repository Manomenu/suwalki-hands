from dataclasses import dataclass

from ebrit_hands.jobs.enums import JobStatus, JobType


@dataclass
class Job:
    status: JobStatus
    job_type: JobType
    identifier: str
