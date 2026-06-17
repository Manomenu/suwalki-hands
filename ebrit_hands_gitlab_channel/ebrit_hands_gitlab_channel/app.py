from fastapi import FastAPI

from ebrit_hands_gitlab_channel.review.router import router as review_router
from ebrit_hands_gitlab_channel.webhook.router import router as webhook_router

app = FastAPI()
app.include_router(webhook_router)
app.include_router(review_router)
