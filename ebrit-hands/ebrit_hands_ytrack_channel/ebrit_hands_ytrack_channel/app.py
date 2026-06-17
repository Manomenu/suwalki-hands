from fastapi import FastAPI

from ebrit_hands_ytrack_channel.api.webhook import router as webhook_router

app = FastAPI()
app.include_router(webhook_router)
