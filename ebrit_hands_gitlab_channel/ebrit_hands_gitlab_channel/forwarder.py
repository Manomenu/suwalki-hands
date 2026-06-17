import logging

import gitlab

from ebrit_hands_library import rest_client
from ebrit_hands_library.contracts.review import MergeRequestChange, ReviewRequest

from ebrit_hands_gitlab_channel.settings import settings

log = logging.getLogger(__name__)


def _enrich(review: ReviewRequest) -> ReviewRequest:
    gl = gitlab.Gitlab(url=f"https://{settings.gitlab_host}", private_token=settings.gitlab_token)
    mr = gl.projects.get(review.project_id).mergerequests.get(review.mr_iid)
    raw_changes = mr.changes().get("changes", [])
    changes = [
        MergeRequestChange(
            old_path=c.get("old_path", ""),
            new_path=c.get("new_path", ""),
            diff=c.get("diff", ""),
        )
        for c in raw_changes
    ]
    return review.model_copy(update={
        "target_branch": mr.target_branch,
        "changes": changes,
    })


async def forward_review(review: ReviewRequest) -> str:
    review = _enrich(review)
    review = review.model_copy(update={"callback_url": f"{settings.gitlab_channel_url}/review-done"})
    data = await rest_client.post(f"{settings.ebrit_hands_url}/reviews", review)
    job_id: str = data["job_id"]
    log.info("Forwarded review project=%s MR!%s → job %s", review.project_id, review.mr_iid, job_id)
    return job_id


async def forward_review_background(review: ReviewRequest) -> None:
    try:
        await forward_review(review)
    except Exception:
        log.exception("Failed to forward review to ebrit_hands")
