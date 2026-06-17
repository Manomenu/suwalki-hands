import logging
import os
from pathlib import Path

import ebrit_hands as _pkg
from openhands.sdk import RemoteConversation

from ebrit_hands.ai.workspaces import UserDockerWorkspace
from ebrit_hands_library.contracts.review import InlineComment
from ebrit_hands import git
from ebrit_hands.jobs import JobStatus, set_job_status
from ebrit_hands.reviews.agents import create_review_agent
from ebrit_hands.reviews.responder import send_result
from ebrit_hands.reviews.schemas import ReviewRequest
from ebrit_hands.settings import settings

log = logging.getLogger(__name__)

# Host path of the ebrit_hands project root (parent of the package dir)
# Mounted into the container so the server can import ebrit_hands.reviews.tools
_EBRIT_HANDS_SRC = str(Path(_pkg.__file__).parent.parent)
_CONTAINER_SRC = "/ebrit_hands_src"
os.environ.setdefault("OH_EXTRA_PYTHON_PATH", _CONTAINER_SRC)


def _read_inline_comments(metadata: Path) -> list[InlineComment]:
    comments_dir = metadata / "inline_comments"
    if not comments_dir.exists():
        return []
    return [
        InlineComment.model_validate_json(f.read_text())
        for f in sorted(comments_dir.glob("*.json"))
    ]


async def process_review(review: ReviewRequest, job_id: str) -> None:
    set_job_status(job_id, JobStatus.IN_PROGRESS)
    try:
        repo_config = settings.get_repo(review.project_id)
        with git.repository(review.discussion_id, repo_config, review.source_branch) as (project, metadata):
            with UserDockerWorkspace(
                volumes=[
                    f"{project}:/workspace/project",
                    f"{metadata}:/workspace/metadata",
                    f"{_EBRIT_HANDS_SRC}:{_CONTAINER_SRC}",
                ],
                forward_env=["OH_EXTRA_PYTHON_PATH"],
            ) as workspace:
                conversation = RemoteConversation(create_review_agent("/workspace/metadata"), workspace)
                changes_text = "\n\n".join(c.to_string() for c in review.changes)
                conversation.send_message(
                    f"""
                    You are reviewing MR: {review.mr_title}

                    Reviewer's instructions: {review.note}

                    Changes:
                    {changes_text}

                    The full repository is cloned at /workspace/project.
                    Use file_editor (view only), glob, and grep to read files for additional context — do NOT edit any files.
                    Post inline review comments using the create_git_inline_comment tool.
                    When finished, write a high-level summary of what you reviewed to /workspace/metadata/review_summary.md.
                    Omit details already covered in inline comments — the summary should be a brief overall assessment only."""
                )
                conversation.run()
                log.info("Agent wrote MR comments for discussion %s.", review.discussion_id)


            inline_comments = _read_inline_comments(metadata)
            summary_file = metadata / "review_summary.md"
            summary = summary_file.read_text() if summary_file.exists() else "Code review complete."

        await send_result(review, job_id, body=summary, inline_comments=inline_comments)
    except Exception:
        set_job_status(job_id, JobStatus.ERROR)
        log.exception("Review job %s failed", job_id)
