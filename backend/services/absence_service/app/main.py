from fastapi import FastAPI
from app.routes import absence_routes, rattrapage_routes, justificatif_routes

app = FastAPI(title="absence_service")

app.include_router(absence_routes.router, prefix="/absences", tags=["absences"])
app.include_router(rattrapage_routes.router, prefix="/rattrapages", tags=["rattrapages"])
app.include_router(justificatif_routes.router, prefix="/justificatifs", tags=["justificatifs"])


@app.get("/")
async def root():
    return {"service": "absence_service", "status": "ok"}
