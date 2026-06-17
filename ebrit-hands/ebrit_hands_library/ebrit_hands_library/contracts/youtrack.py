from pydantic import BaseModel


class YouTrackComment(BaseModel):
    id: str
    text: str
    author_login: str


class YouTrackTask(BaseModel):
    issue_id: str
    title: str
    description: str | None
    source_branch: str | None
    comments: list[YouTrackComment]
    gitlab_project_id: int = 0
