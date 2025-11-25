"""
Routes pour les groupes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.groupe import Groupe

router = APIRouter()

@router.get("/", response_model=List[dict])
def get_all_groupes(db: Session = Depends(get_db)):
    """Récupère tous les groupes"""
    try:
        groupes = db.query(Groupe).all()
        return [{"id": g.id, "nom": g.nom, "niveau_id": g.niveau_id, "departement_id": g.departement_id} for g in groupes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{groupe_id}", response_model=dict)
def get_groupe(groupe_id: int, db: Session = Depends(get_db)):
    """Récupère un groupe par son ID"""
    groupe = db.query(Groupe).filter(Groupe.id == groupe_id).first()
    if not groupe:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    return {"id": groupe.id, "nom": groupe.nom, "niveau_id": groupe.niveau_id, "departement_id": groupe.departement_id}
