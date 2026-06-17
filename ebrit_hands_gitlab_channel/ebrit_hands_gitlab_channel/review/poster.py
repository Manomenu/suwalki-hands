import hashlib
import logging

import gitlab

from ebrit_hands_library.contracts.review import InlineComment, ReviewResult

from ebrit_hands_gitlab_channel.settings import settings

log = logging.getLogger(__name__)


def _line_code(file_path: str, old_line: int | None, new_line: int | None) -> str:
    file_hash = hashlib.sha1(file_path.encode()).hexdigest()
    return f"{file_hash}_{old_line or 0}_{new_line or 0}"


def _build_position(ic: InlineComment, refs: dict) -> dict:
    position: dict = {
        "position_type": "text",
        "base_sha": refs["base_sha"],
        "start_sha": refs["start_sha"],
        "head_sha": refs["head_sha"],
        "new_path": ic.file_path,
        "old_path": ic.file_path,
    }
    if ic.new_line is not None:
        position["new_line"] = ic.new_line
    if ic.old_line is not None:
        position["old_line"] = ic.old_line
    position["line_code"] = _line_code(ic.file_path, ic.old_line, ic.new_line)

    has_range = ic.new_line_start is not None or ic.old_line_start is not None
    if has_range:
        line_type = "new" if ic.new_line is not None else "old"
        position["line_range"] = {
            "start": {
                "line_code": _line_code(ic.file_path, ic.old_line_start, ic.new_line_start),
                "type": "new" if ic.new_line_start is not None else "old",
            },
            "end": {
                "line_code": _line_code(ic.file_path, ic.old_line, ic.new_line),
                "type": line_type,
            },
        }
    return position


def post_review_reply(result: ReviewResult) -> None:
    gl = gitlab.Gitlab(url=f"https://{settings.gitlab_host}", private_token=settings.gitlab_token)
    mr = gl.projects.get(result.project_id).mergerequests.get(result.mr_iid)

    if result.inline_comments:
        refs = mr.diff_refs
        for ic in result.inline_comments:
            try:
                mr.discussions.create({"body": ic.comment, "position": _build_position(ic, refs)})
            except Exception:
                log.exception("Failed to post inline comment on %s:%s", ic.file_path, ic.new_line or ic.old_line)

    mr.discussions.get(result.discussion_id).notes.create({"body": result.body})
    log.info(
        "Posted review reply project=%s MR!%s discussion=%s inline=%d job=%s",
        result.project_id,
        result.mr_iid,
        result.discussion_id,
        len(result.inline_comments),
        result.job_id,
    )
