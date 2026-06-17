from fastapi import FastAPI

from ebrit_hands.jobs.router import router as jobs_router
from ebrit_hands.tasks.router import router as tasks_router
from ebrit_hands.reviews.router import router as reviews_router

app = FastAPI()
app.include_router(jobs_router)
app.include_router(tasks_router)
app.include_router(reviews_router)
