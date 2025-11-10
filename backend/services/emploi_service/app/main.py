from fastapi import FastAPI
from app.routes import salle_routes, emploi_temps_routes, absence_routes

app = FastAPI(title="emploi_service")

app.include_router(salle_routes.router, prefix="/salles", tags=["salles"])
app.include_router(emploi_temps_routes.router, prefix="/emplois", tags=["emplois"])
app.include_router(absence_routes.router, prefix="/absences", tags=["absences"])


@app.get("/")
async def root():
    return {"service": "emploi_service", "status": "ok"}
