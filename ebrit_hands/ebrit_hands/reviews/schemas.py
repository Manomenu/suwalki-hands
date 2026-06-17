from ebrit_hands_library.contracts.review import ReviewRequest, ReviewResult  # noqa: F401

from pydantic import BaseModel


class ReviewResponse(BaseModel):
    job_id: str
    status: str
