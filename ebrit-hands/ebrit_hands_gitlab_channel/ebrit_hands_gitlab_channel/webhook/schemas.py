from pydantic import BaseModel


class _GitLabUser(BaseModel):
    id: int
    username: str


class _GitLabObjectAttributes(BaseModel):
    id: int
    note: str
    noteable_type: str
    discussion_id: str


class _GitLabMergeRequest(BaseModel):
    iid: int
    title: str
    source_branch: str


class GitLabCommentPayload(BaseModel):
    object_kind: str
    project_id: int
    user: _GitLabUser
    object_attributes: _GitLabObjectAttributes
    merge_request: _GitLabMergeRequest | None = None


class WebhookResponse(BaseModel):
    status: str
    job_id: str | None = None
