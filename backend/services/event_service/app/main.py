from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.event_routes import router as event_router

app = FastAPI(title="event_service", version="0.1")
# Enable CORS for local frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200", "http://localhost:64073"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(event_router, prefix="/events", tags=["events"])

@app.get("/")
def root():
    return {"service": "event_service", "status": "ok"}
