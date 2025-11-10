from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.emploi_temps import EmploiTempsCreate, EmploiTempsRead
from app.crud.emploi_temps_crud import get_emploi, get_emplois, create_emploi, delete_emploi
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[EmploiTempsRead])
def list_emplois(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_emplois(db, skip=skip, limit=limit)


@router.post("/", response_model=EmploiTempsRead)
def create(e: EmploiTempsCreate, db: Session = Depends(get_db)):
    try:
        return create_emploi(db, e)
    except ValueError as ex:
        raise HTTPException(status_code=409, detail=str(ex))


@router.get("/{emploi_id}", response_model=EmploiTempsRead)
def read(emploi_id: int, db: Session = Depends(get_db)):
    obj = get_emploi(db, emploi_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Emploi not found")
    return obj


@router.delete("/{emploi_id}", response_model=EmploiTempsRead)
def delete(emploi_id: int, db: Session = Depends(get_db)):
    obj = delete_emploi(db, emploi_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Emploi not found")
    return obj
