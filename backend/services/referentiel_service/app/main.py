import sys
import os

# Ensure the service package directory is first on sys.path so our local `app` package
# is imported instead of any top-level `app` package installed in site-packages.
SERVICE_ROOT = os.path.dirname(os.path.dirname(__file__))
if SERVICE_ROOT not in sys.path:
    sys.path.insert(0, SERVICE_ROOT)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import departement_routes, matiere_routes, enseignant_routes, etudiant_routes, salle_routes, setup_routes, niveau_routes, groupe_routes

app = FastAPI(title="referentiel_service")

# Development CORS: allow the frontend dev server and local hosts
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "http://localhost",
        "http://127.0.0.1",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(departement_routes.router, prefix="/departements", tags=["departements"])
app.include_router(matiere_routes.router, prefix="/matieres", tags=["matieres"])
# alias: some clients expect the path '/specialites' (French variant). Provide compatibility.
app.include_router(matiere_routes.router, prefix="/specialites", tags=["matieres"])
app.include_router(enseignant_routes.router, prefix="/enseignants", tags=["enseignants"])
app.include_router(etudiant_routes.router, prefix="/etudiants", tags=["etudiants"])
app.include_router(salle_routes.router, prefix="/salles", tags=["salles"])
app.include_router(niveau_routes.router, prefix="/niveaux", tags=["niveaux"])
app.include_router(groupe_routes.router, prefix="/groupes", tags=["groupes"])
app.include_router(setup_routes.router, prefix="/api", tags=["setup"])

@app.get("/")
async def root():
    return {"service": "referentiel_service", "status": "ok"}
