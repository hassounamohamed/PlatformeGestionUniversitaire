from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.salle import SalleCreate, SalleRead
from app.crud.salle_crud import get_salle, get_salles, create_salle, delete_salle, update_salle
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[SalleRead])
def list_salles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_salles(db, skip=skip, limit=limit)


@router.post("/", response_model=SalleRead)
def create(s: SalleCreate, db: Session = Depends(get_db)):
    existing = db.query().filter
    return create_salle(db, s)


@router.get("/{salle_id}", response_model=SalleRead)
def read(salle_id: int, db: Session = Depends(get_db)):
    obj = get_salle(db, salle_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Salle not found")
    return obj


@router.delete("/{salle_id}", response_model=SalleRead)
def delete(salle_id: int, db: Session = Depends(get_db)):
    obj = delete_salle(db, salle_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Salle not found")
    return obj


@router.put("/{salle_id}", response_model=SalleRead)
def update(salle_id: int, s: SalleCreate, db: Session = Depends(get_db)):
    obj = update_salle(db, salle_id, code=s.code, type=s.type, capacite=s.capacite)
    if not obj:
        raise HTTPException(status_code=404, detail="Salle not found")
    return obj
