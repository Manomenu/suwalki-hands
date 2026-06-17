import logging

from fastapi import APIRouter, HTTPException

from ebrit_hands.jobs.registry import get_job_status, get_jobs

log = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs")


@router.get("/")
async def list_jobs() -> list[dict]:
    return [
        {"job_id": job_id, "status": job.status, "job_type": job.job_type, "identifier": job.identifier}
        for job_id, job in get_jobs().items()
    ]


@router.get("/{job_id}/status")
async def job_status(job_id: str) -> dict:
    status = get_job_status(job_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": status}
