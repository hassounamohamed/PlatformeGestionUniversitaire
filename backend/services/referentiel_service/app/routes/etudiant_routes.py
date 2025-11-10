from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import StreamingResponse
import csv
import io

from app.schemas.etudiant import EtudiantCreate, EtudiantRead
from app.crud.etudiant_crud import get_etudiant, get_etudiants, create_etudiant, delete_etudiant
from app.core.database import get_db
from app.crud.etudiant_crud import update_etudiant
from app.core.admin import admin_required

router = APIRouter()

@router.get("/", response_model=List[EtudiantRead])
def list_etudiants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_etudiants(db, skip=skip, limit=limit)

@router.post("/", response_model=EtudiantRead)
def create(e: EtudiantCreate, db: Session = Depends(get_db), _=Depends(admin_required)):
    return create_etudiant(db, e)


@router.post("/import", response_model=dict)
def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db), _=Depends(admin_required)):
    """Import students from uploaded CSV file. Expected headers: nom,prenom,email,groupe_id,specialite_id

    Returns a summary: {created: n, errors: [{row: i, error: msg}, ...]}
    """
    text = file.file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(text))
    created = 0
    errors = []
    for i, row in enumerate(reader, start=1):
        try:
            payload = {k: v if v != '' else None for k, v in row.items()}
            # convert numeric fields
            if payload.get('groupe_id'):
                payload['groupe_id'] = int(payload['groupe_id'])
            if payload.get('specialite_id'):
                payload['specialite_id'] = int(payload['specialite_id'])
            e = EtudiantCreate(**payload)
            create_etudiant(db, e)
            created += 1
        except Exception as ex:
            errors.append({"row": i, "error": str(ex), "data": row})
    return {"created": created, "errors": errors}


@router.get("/export")
def export_csv(db: Session = Depends(get_db), _=Depends(admin_required)):
    """Export all students as CSV."""
    students = get_etudiants(db, skip=0, limit=1000000)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "nom", "prenom", "email", "groupe_id", "specialite_id"]) 
    for s in students:
        writer.writerow([s.id, s.nom, s.prenom, s.email, s.groupe_id, s.specialite_id])
    output.seek(0)
    return StreamingResponse(io.StringIO(output.read()), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=etudiants.csv"})

@router.get("/{etudiant_id}", response_model=EtudiantRead)
def read(etudiant_id: int, db: Session = Depends(get_db)):
    obj = get_etudiant(db, etudiant_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return obj

@router.delete("/{etudiant_id}", response_model=EtudiantRead)
def delete(e_id: int, db: Session = Depends(get_db)):
    obj = delete_etudiant(db, e_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return obj


@router.patch("/{etudiant_id}", response_model=EtudiantRead)
def patch(etudiant_id: int, patch: EtudiantCreate, db: Session = Depends(get_db)):
    obj = update_etudiant(db, etudiant_id, patch.model_dump(exclude_none=True))
    if not obj:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return obj
