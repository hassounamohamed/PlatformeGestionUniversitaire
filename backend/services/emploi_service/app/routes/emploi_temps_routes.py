from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.schemas.emploi_temps import EmploiTempsCreate, EmploiTempsRead
from app.crud.emploi_temps_crud import get_emploi, get_emplois, create_emploi, delete_emploi
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[EmploiTempsRead])
def list_emplois(
    skip: int = 0,
    limit: int = 100,
    enseignant_id: Optional[int] = None,
    groupe_id: Optional[int] = None,
    enseignant_nom: Optional[str] = None,
    groupe_nom: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db)
):
    # Resolve names to ids via referentiel_service if provided
    import httpx

    if enseignant_nom and not enseignant_id:
        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.get("http://127.0.0.1:8003/enseignants/")
                resp.raise_for_status()
                items = resp.json()
                # try match on 'prenom nom' or 'nom prenom' or full_name
                for it in items:
                    full1 = f"{it.get('prenom','')} {it.get('nom','')}".strip()
                    full2 = f"{it.get('nom','')} {it.get('prenom','')}".strip()
                    if enseignant_nom.lower() in (full1.lower(), full2.lower(), it.get('email','').lower()):
                        enseignant_id = it.get('id')
                        break
        except Exception:
            pass

    if groupe_nom and not groupe_id:
        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.get("http://127.0.0.1:8003/groupes/")
                resp.raise_for_status()
                items = resp.json()
                for it in items:
                    if groupe_nom.lower() == str(it.get('nom','')).lower():
                        groupe_id = it.get('id')
                        break
        except Exception:
            pass

    return get_emplois(db, skip=skip, limit=limit, enseignant_id=enseignant_id, groupe_id=groupe_id, date_from=date_from, date_to=date_to)


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
