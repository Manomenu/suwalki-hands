import asyncio
import logging
import threading

from fastapi import APIRouter

from ebrit_hands.jobs import JobType, create_job
from ebrit_hands.tasks.runner import process_task
from ebrit_hands.tasks.schemas import TaskRequest, TaskResponse

log = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks")


@router.post("", response_model=TaskResponse, status_code=202)
async def run_task(task: TaskRequest) -> TaskResponse:
    job_id = create_job(JobType.TASK, task.issue_id)
    log.info("Accepted task %s: %s", task.issue_id, task.title)
    threading.Thread(
        target=asyncio.run,
        args=(process_task(task, job_id),),
        daemon=True,
    ).start()
    return TaskResponse(job_id=job_id, status="accepted")
