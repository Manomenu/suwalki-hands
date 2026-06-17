from pydantic import BaseModel

from ebrit_hands_ytrack_channel.settings import settings


class WebhookResponse(BaseModel):
    status: str
    issue_id: str | None = None
    job_id: str | None = None


class MockWebhookRequest(BaseModel):
    issue_id: str = settings.mock_youtrack_issue_id
    title: str = settings.mock_youtrack_title
    description: str = settings.mock_youtrack_description
    source_branch: str = settings.mock_youtrack_source_branch
    assignee_login: str = settings.mock_youtrack_assignee_login
    gitlab_project_id: int = 0
