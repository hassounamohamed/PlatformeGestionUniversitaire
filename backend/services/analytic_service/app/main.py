from fastapi import FastAPI
from .routes.analytic_routes import router as analytic_router

app = FastAPI(title="analytic_service", version="0.1")

app.include_router(analytic_router, prefix="/analytics", tags=["analytics"]) 

@app.get("/")
def root():
    return {"service": "analytic_service", "status": "ok"}
