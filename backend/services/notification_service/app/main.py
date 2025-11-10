from fastapi import FastAPI
from app.routes import notification_router

app = FastAPI(title="notification_service")

app.include_router(notification_router, prefix="/notifications", tags=["notifications"])


@app.get("/")
async def root():
    return {"service": "notification_service", "status": "ok"}
