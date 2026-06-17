import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request

from ebrit_hands_ytrack_channel.api.schemas import MockWebhookRequest, WebhookResponse
from ebrit_hands_ytrack_channel.forwarder import forward_task, forward_task_background
from ebrit_hands_ytrack_channel.settings import settings
from ebrit_hands_ytrack_channel.youtrack.mock import build_payload
from ebrit_hands_ytrack_channel.youtrack.parser import parse_webhook

log = logging.getLogger(__name__)

router = APIRouter()


@router.post("/webhook", response_model=WebhookResponse)
async def receive_webhook(request: Request, background_tasks: BackgroundTasks) -> WebhookResponse:
    payload = await request.json()
    task = parse_webhook(payload)

    if task is None:
        return WebhookResponse(status="ignored")

    log.info("Received task %s: %s", task.issue_id, task.title)
    log.debug("Task details: %s", task.model_dump_json())
    background_tasks.add_task(forward_task_background, task)

    return WebhookResponse(status="ok", issue_id=task.issue_id)


@router.post("/webhook/mock", response_model=WebhookResponse)
async def mock_webhook(req: MockWebhookRequest = MockWebhookRequest()) -> WebhookResponse:
    assignee = req.assignee_login or settings.youtrack_bot_login
    payload = build_payload(req.issue_id, req.title, req.description, req.source_branch, assignee)
    task = parse_webhook(payload)

    if task is None:
        return WebhookResponse(status="ignored")

    task = task.model_copy(update={"gitlab_project_id": req.gitlab_project_id})
    log.info("Mock task %s: %s (project_id=%s)", task.issue_id, task.title, task.gitlab_project_id)
    try:
        job_id = await forward_task(task)
    except Exception:
        log.exception("Failed to forward mock task %s to ebrit-hands", task.issue_id)
        raise HTTPException(status_code=502, detail="ebrit-hands unreachable")

    return WebhookResponse(status="ok", issue_id=task.issue_id, job_id=job_id)
