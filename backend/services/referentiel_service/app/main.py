import sys
import os

# Ensure the service package directory is first on sys.path so our local `app` package
# is imported instead of any top-level `app` package installed in site-packages.
SERVICE_ROOT = os.path.dirname(os.path.dirname(__file__))
if SERVICE_ROOT not in sys.path:
    sys.path.insert(0, SERVICE_ROOT)

from fastapi import FastAPI
from app.routes import departement_routes, matiere_routes, enseignant_routes, etudiant_routes, salle_routes

app = FastAPI(title="referentiel_service")

app.include_router(departement_routes.router, prefix="/departements", tags=["departements"])
app.include_router(matiere_routes.router, prefix="/matieres", tags=["matieres"])
app.include_router(enseignant_routes.router, prefix="/enseignants", tags=["enseignants"])
app.include_router(etudiant_routes.router, prefix="/etudiants", tags=["etudiants"])
app.include_router(salle_routes.router, prefix="/salles", tags=["salles"])

@app.get("/")
async def root():
    return {"service": "referentiel_service", "status": "ok"}
