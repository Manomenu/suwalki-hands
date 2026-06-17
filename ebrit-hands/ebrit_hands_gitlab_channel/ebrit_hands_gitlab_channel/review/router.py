from fastapi import APIRouter

from ebrit_hands_library.contracts.review import ReviewResult

from ebrit_hands_gitlab_channel.review.poster import post_review_reply

router = APIRouter()


@router.post("/review-done")
async def review_done(result: ReviewResult) -> dict:
    post_review_reply(result)
    return {"ok": True}
