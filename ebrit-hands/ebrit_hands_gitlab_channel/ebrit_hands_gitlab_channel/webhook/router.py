import logging

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request

from ebrit_hands_gitlab_channel.forwarder import forward_review_background
from ebrit_hands_gitlab_channel.settings import settings
from ebrit_hands_gitlab_channel.review.parser import try_parse_review_request
from ebrit_hands_gitlab_channel.webhook.schemas import WebhookResponse

log = logging.getLogger(__name__)

router = APIRouter()


@router.post("/webhook", response_model=WebhookResponse)
async def receive_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_gitlab_token: str | None = Header(default=None),
) -> WebhookResponse:
    if settings.gitlab_webhook_secret and x_gitlab_token != settings.gitlab_webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    payload = await request.json()
    review = try_parse_review_request(payload)

    if review is None:
        return WebhookResponse(status="ignored")

    log.info(
        "Received @review on project=%s MR!%s note=%s",
        review.project_id,
        review.mr_iid,
        review.note_id,
    )
    background_tasks.add_task(forward_review_background, review)

    return WebhookResponse(status="ok")
