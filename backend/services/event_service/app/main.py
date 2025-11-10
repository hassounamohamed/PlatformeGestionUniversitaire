from fastapi import FastAPI
from .routes.event_routes import router as event_router

app = FastAPI(title="event_service", version="0.1")
app.include_router(event_router, prefix="/events", tags=["events"])

@app.get("/")
def root():
    return {"service": "event_service", "status": "ok"}
