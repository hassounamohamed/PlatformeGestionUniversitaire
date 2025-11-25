from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.matiere import MatiereCreate, MatiereRead
from fastapi import Body
from app.crud.matiere_crud import get_matiere, get_matieres, create_matiere, delete_matiere
from app.core.database import get_db
from app.schemas.matiere import MatiereUpdate
from app.crud.matiere_crud import update_matiere

router = APIRouter()

@router.get("/", response_model=List[MatiereRead])
def list_matieres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_matieres(db, skip=skip, limit=limit)

@router.post("/", response_model=MatiereRead)
def create(payload: dict = Body(...), db: Session = Depends(get_db)):
    # Accept {name: ...} or {nom: ...}
    nom = payload.get('nom') or payload.get('name')
    if not nom:
        raise HTTPException(status_code=422, detail="Missing 'nom' or 'name'")
    m = MatiereCreate(nom=nom, niveau_id=payload.get('niveau_id'), enseignant_id=payload.get('enseignant_id'))
    return create_matiere(db, m)

@router.get("/{matiere_id}", response_model=MatiereRead)
def read(matiere_id: int, db: Session = Depends(get_db)):
    obj = get_matiere(db, matiere_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Matiere not found")
    return obj

@router.delete("/{matiere_id}", response_model=MatiereRead)
def delete(matiere_id: int, db: Session = Depends(get_db)):
    obj = delete_matiere(db, matiere_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Matiere not found")
    return obj


@router.patch("/{matiere_id}", response_model=MatiereRead)
def patch(matiere_id: int, patch: MatiereUpdate, db: Session = Depends(get_db)):
    obj = update_matiere(db, matiere_id, patch.model_dump(exclude_none=True))
    if not obj:
        raise HTTPException(status_code=404, detail="Matiere not found")
    return obj
