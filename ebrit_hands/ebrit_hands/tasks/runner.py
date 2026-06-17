import logging

from ebrit_hands.tasks.schemas import TaskRequest
from lmnr import observe
from openhands.sdk import RemoteConversation

from ebrit_hands.ai.workspaces import UserDockerWorkspace
from ebrit_hands.tasks.agents import create_task_agent
from ebrit_hands.ai.completions import generate_branch_name
from ebrit_hands import git
from ebrit_hands.image_resolver import resolve_server_image
from ebrit_hands.jobs import JobStatus, set_job_status
from ebrit_hands.settings import settings

log = logging.getLogger(__name__)


@observe(name="process_task", tags=["task"])
async def process_task(task: TaskRequest, job_id: str) -> str:
    set_job_status(job_id, JobStatus.IN_PROGRESS)
    try:
        repo_config = settings.get_repo(task.gitlab_project_id)
        with git.repository(task.issue_id, repo=repo_config, branch=task.source_branch) as (project, metadata):
            branch_name = generate_branch_name(task.issue_id, task.title, task.description or "")
            branch = git.switch_branch(project, task.issue_id, branch_name)

            with UserDockerWorkspace(server_image=resolve_server_image(repo_config.image), volumes=[f"{project}:/workspace/project", f"{metadata}:/workspace/metadata"]) as workspace:
                conversation = RemoteConversation(create_task_agent(), workspace)

                conversation.send_message(f"/complete-task title: {task.title} description: {task.description or ''}")
                conversation.run()

                log.info("Agent completed task %s.", task.issue_id)

                conversation.send_message("/mr_description")
                conversation.run()

                log.info("Agent wrote MR description for task %s.", task.issue_id)

            git.commit_leftovers(task.issue_id, project)
            git.save_on_remote(project, branch)

            desc_file = metadata / "mr_description.md"
            mr_description = desc_file.read_text() if desc_file.exists() else ""

        target_branch = task.source_branch or repo_config.default_branch
        mr_url = git.create_merge_request(branch, target_branch, task.issue_id, task.title, mr_description, repo=repo_config)
        log.info("Completed task %s on branch %s, MR: %s", task.issue_id, branch, mr_url)

        set_job_status(job_id, JobStatus.FINISHED)
        return branch
    except Exception:
        set_job_status(job_id, JobStatus.ERROR)
        log.exception("Task %s failed", task.issue_id)
        raise
