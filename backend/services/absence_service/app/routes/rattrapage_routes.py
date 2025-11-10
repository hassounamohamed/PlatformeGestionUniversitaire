from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.rattrapage import RattrapageCreate, RattrapageRead
from app.crud.rattrapage_crud import get_rattrapage, get_rattrapages, create_rattrapage, delete_rattrapage
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[RattrapageRead])
def list_rattrapages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_rattrapages(db, skip=skip, limit=limit)


@router.post("/", response_model=RattrapageRead)
def create(r: RattrapageCreate, db: Session = Depends(get_db)):
    return create_rattrapage(db, r)


@router.get("/{r_id}", response_model=RattrapageRead)
def read(r_id: int, db: Session = Depends(get_db)):
    obj = get_rattrapage(db, r_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Rattrapage not found")
    return obj


@router.delete("/{r_id}", response_model=RattrapageRead)
def delete(r_id: int, db: Session = Depends(get_db)):
    obj = delete_rattrapage(db, r_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Rattrapage not found")
    return obj
