from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import salle_routes, emploi_temps_routes, absence_routes

app = FastAPI(title="emploi_service")

# CORS
app.add_middleware(
    CORSMiddleware,
    # During local development allow the frontend dev server and localhost hosts.
    # Use a permissive policy here to avoid CORS issues while developing the UI.
    # For production, narrow this to the real frontend origin(s).
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(salle_routes.router, prefix="/salles", tags=["salles"])
app.include_router(emploi_temps_routes.router, prefix="/emplois", tags=["emplois"])
app.include_router(absence_routes.router, prefix="/absences", tags=["absences"])


@app.get("/")
async def root():
    return {"service": "emploi_service", "status": "ok"}
