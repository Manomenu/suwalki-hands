from pydantic import BaseModel

from ebrit_hands_library.contracts.youtrack import YouTrackTask


class TaskResponse(BaseModel):
    job_id: str
    status: str

TaskRequest = YouTrackTask
