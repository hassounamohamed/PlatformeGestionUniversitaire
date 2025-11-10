from fastapi import FastAPI
from .routes.message_routes import router as message_router

app = FastAPI(title="messaging_service", version="0.1")

app.include_router(message_router, prefix="/messages", tags=["messages"]) 

@app.get("/")
def root():
    return {"service": "messaging_service", "status": "ok"}
