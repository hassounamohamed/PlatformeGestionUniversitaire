from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# use relative imports inside the `app` package so running
# `uvicorn app.main:app` resolves local modules correctly
from . import logging_config
# Central logging configuration shared across services
from fastapi import FastAPI

app = FastAPI()

from .api import auth
from .db.init_db import init_db

app = FastAPI(
    title="Auth Service",
    description="Service d'authentification et gestion des utilisateurs",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

@app.on_event("startup")
async def startup_event():
    """Initialisation de la base de données au démarrage"""
    await init_db()

@app.get("/")
async def root():
    return {"message": "Auth Service is running", "service": "auth_service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth_service"}