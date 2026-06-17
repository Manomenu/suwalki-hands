import uuid

from ebrit_hands.jobs.enums import JobStatus, JobType
from ebrit_hands.jobs.models import Job

_registry: dict[str, Job] = {}


def create_job(job_type: JobType, identifier: str) -> str:
    job_id = str(uuid.uuid4())
    _registry[job_id] = Job(status=JobStatus.SUBMITTED, job_type=job_type, identifier=identifier)
    return job_id


def get_job_status(job_id: str) -> JobStatus | None:
    job = _registry.get(job_id)
    return job.status if job else None


def get_jobs() -> dict[str, Job]:
    return dict(_registry)


def set_job_status(job_id: str, status: JobStatus) -> None:
    if job := _registry.get(job_id):
        job.status = status
