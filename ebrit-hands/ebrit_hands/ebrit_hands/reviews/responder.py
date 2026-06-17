import logging

from ebrit_hands_library import rest_client
from ebrit_hands_library.contracts.review import InlineComment
from ebrit_hands.jobs import JobStatus, set_job_status
from ebrit_hands.reviews.schemas import ReviewRequest, ReviewResult

log = logging.getLogger(__name__)


async def send_result(
    review: ReviewRequest,
    job_id: str,
    body: str,
    inline_comments: list[InlineComment] | None = None,
) -> None:
    if not review.callback_url:
        log.warning("No callback_url for review job=%s — result discarded", job_id)
        set_job_status(job_id, JobStatus.FINISHED)
        return

    result = ReviewResult(
        job_id=job_id,
        project_id=review.project_id,
        mr_iid=review.mr_iid,
        discussion_id=review.discussion_id,
        body=body,
        status="finished",
        inline_comments=inline_comments or [],
    )
    await rest_client.post(review.callback_url, result)
    log.info("Sent review result to callback job=%s, inline_comments=%d", job_id, len(result.inline_comments))
    set_job_status(job_id, JobStatus.FINISHED)
