from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.justificatif import JustificatifCreate, JustificatifRead
from app.crud.justificatif_crud import get_justificatif, get_justificatifs, create_justificatif, update_justificatif, delete_justificatif
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[JustificatifRead])
def list_justificatifs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_justificatifs(db, skip=skip, limit=limit)


@router.post("/", response_model=JustificatifRead)
def create(j: JustificatifCreate, db: Session = Depends(get_db)):
    return create_justificatif(db, j)


@router.get("/{j_id}", response_model=JustificatifRead)
def read(j_id: int, db: Session = Depends(get_db)):
    obj = get_justificatif(db, j_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Justificatif not found")
    return obj


@router.patch("/{j_id}", response_model=JustificatifRead)
def patch(j_id: int, patch: dict, db: Session = Depends(get_db)):
    obj = update_justificatif(db, j_id, patch)
    if not obj:
        raise HTTPException(status_code=404, detail="Justificatif not found")
    return obj


@router.delete("/{j_id}", response_model=JustificatifRead)
def delete(j_id: int, db: Session = Depends(get_db)):
    obj = delete_justificatif(db, j_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Justificatif not found")
    return obj
