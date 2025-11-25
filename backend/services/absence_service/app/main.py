from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import absence_routes, rattrapage_routes, justificatif_routes

app = FastAPI(title="absence_service")

# Development CORS: allow all origins to simplify local testing from Angular dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(absence_routes.router, prefix="/absences", tags=["absences"])
app.include_router(rattrapage_routes.router, prefix="/rattrapages", tags=["rattrapages"])
app.include_router(justificatif_routes.router, prefix="/justificatifs", tags=["justificatifs"])


@app.get("/")
async def root():
    return {"service": "absence_service", "status": "ok"}
