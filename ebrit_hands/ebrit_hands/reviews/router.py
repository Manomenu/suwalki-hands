import asyncio
import logging
import threading

from fastapi import APIRouter

from ebrit_hands.jobs import JobType, create_job
from ebrit_hands.reviews.runner import process_review
from ebrit_hands.reviews.schemas import ReviewResponse, ReviewRequest

log = logging.getLogger(__name__)

router = APIRouter(prefix="/reviews")


@router.post("", response_model=ReviewResponse, status_code=202)
async def run_review(review: ReviewRequest) -> ReviewResponse:
    job_id = create_job(JobType.REVIEW, f"{review.mr_title} #{str(review.note_id)[-5:]}")
    log.info(
        "Accepted review project=%s MR!%s note=%s branch=%s",
        review.project_id,
        review.mr_iid,
        review.note_id,
        review.source_branch,
    )
    threading.Thread(
        target=asyncio.run,
        args=(process_review(review, job_id),),
        daemon=True,
    ).start()
    return ReviewResponse(job_id=job_id, status="accepted")
