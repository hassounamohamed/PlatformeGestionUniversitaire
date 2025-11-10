from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.departement import DepartementCreate, DepartementRead
from app.crud.departement_crud import get_departement, get_departements, create_departement, delete_departement, update_departement
from app.core.database import get_db
from app.models.departement import Departement
from app.core.admin import admin_required

router = APIRouter()


@router.get("/", response_model=List[DepartementRead])
def list_departements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_departements(db, skip=skip, limit=limit)


@router.post("/", response_model=DepartementRead)
def create(d: DepartementCreate, db: Session = Depends(get_db), _=Depends(admin_required)):
    # simple uniqueness check by name
    existing = db.query(Departement).filter(Departement.nom == d.nom).first()
    if existing:
        raise HTTPException(status_code=400, detail="Departement with this name already exists")
    return create_departement(db, d)


@router.get("/{departement_id}", response_model=DepartementRead)
def read(departement_id: int, db: Session = Depends(get_db)):
    obj = get_departement(db, departement_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Departement not found")
    return obj


@router.delete("/{departement_id}", response_model=DepartementRead)
def delete(d_id: int, db: Session = Depends(get_db)):
    obj = delete_departement(db, d_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Departement not found")
    return obj


@router.put("/{departement_id}", response_model=DepartementRead)
def update(departement_id: int, d: DepartementCreate, db: Session = Depends(get_db)):
    obj = update_departement(db, departement_id, d.nom)
    if not obj:
        raise HTTPException(status_code=404, detail="Departement not found")
    return obj
