import logging

from ebrit_hands_library import rest_client
from ebrit_hands_library.contracts.youtrack import YouTrackTask

from ebrit_hands_ytrack_channel.settings import settings

log = logging.getLogger(__name__)


async def forward_task(task: YouTrackTask) -> str:
    data = await rest_client.post(f"{settings.ebrit_hands_url}/tasks", task)
    job_id: str = data["job_id"]
    log.info("Forwarded task %s → job %s", task.issue_id, job_id)
    return job_id


async def forward_task_background(task: YouTrackTask) -> None:
    try:
        await forward_task(task)
    except Exception:
        log.exception("Failed to forward task %s to ebrit-hands", task.issue_id)
