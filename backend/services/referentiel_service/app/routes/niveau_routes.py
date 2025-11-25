"""
Routes pour les niveaux
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.niveau import Niveau

router = APIRouter()

@router.get("/", response_model=List[dict])
def get_all_niveaux(db: Session = Depends(get_db)):
    """Récupère tous les niveaux"""
    try:
        niveaux = db.query(Niveau).all()
        return [{"id": n.id, "nom": n.nom, "departement_id": n.departement_id} for n in niveaux]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{niveau_id}", response_model=dict)
def get_niveau(niveau_id: int, db: Session = Depends(get_db)):
    """Récupère un niveau par son ID"""
    niveau = db.query(Niveau).filter(Niveau.id == niveau_id).first()
    if not niveau:
        raise HTTPException(status_code=404, detail="Niveau non trouvé")
    return {"id": niveau.id, "nom": niveau.nom, "departement_id": niveau.departement_id}
