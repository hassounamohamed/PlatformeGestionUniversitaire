from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.absence import AbsenceCreate, AbsenceRead
from app.crud.absence_crud import get_absence, get_absences, create_absence, delete_absence, update_absence
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[AbsenceRead])
def list_absences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_absences(db, skip=skip, limit=limit)


@router.post("/", response_model=AbsenceRead)
def create(a: AbsenceCreate, db: Session = Depends(get_db)):
    return create_absence(db, a)


@router.get("/{absence_id}", response_model=AbsenceRead)
def read(absence_id: int, db: Session = Depends(get_db)):
    obj = get_absence(db, absence_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Absence not found")
    return obj


@router.patch("/{absence_id}", response_model=AbsenceRead)
def patch(absence_id: int, patch: dict, db: Session = Depends(get_db)):
    obj = update_absence(db, absence_id, patch)
    if not obj:
        raise HTTPException(status_code=404, detail="Absence not found")
    return obj


@router.delete("/{absence_id}", response_model=AbsenceRead)
def delete(absence_id: int, db: Session = Depends(get_db)):
    obj = delete_absence(db, absence_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Absence not found")
    return obj
