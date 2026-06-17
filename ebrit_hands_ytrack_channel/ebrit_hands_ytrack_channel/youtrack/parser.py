from ebrit_hands_library.contracts.youtrack import YouTrackComment, YouTrackTask

from ebrit_hands_ytrack_channel.settings import settings


def extract_task(payload: dict) -> YouTrackTask | None:
    issue = payload.get("issue", {})
    if not issue:
        return None

    source_branch: str | None = None
    for field in issue.get("customFields", []):
        if field.get("name", "").lower() in ("branch", "source branch", "vcs branch"):
            source_branch = field.get("value")
            break

    comments = [
        YouTrackComment(
            id=c.get("id", ""),
            text=c.get("text", ""),
            author_login=c.get("author", {}).get("login", ""),
        )
        for c in issue.get("comments", [])
    ]

    return YouTrackTask(
        issue_id=issue.get("id", ""),
        title=issue.get("summary", ""),
        description=issue.get("description"),
        source_branch=source_branch,
        comments=comments,
    )


def is_bot_assigned(payload: dict) -> bool:
    if not settings.youtrack_bot_login:
        return True
    for change in payload.get("change", {}).get("fields", []):
        if change.get("name") == "Assignee":
            if any(v.get("login") == settings.youtrack_bot_login for v in change.get("added", [])):
                return True
    return False


def parse_webhook(payload: dict) -> YouTrackTask | None:
    if not is_bot_assigned(payload):
        return None
    return extract_task(payload)
