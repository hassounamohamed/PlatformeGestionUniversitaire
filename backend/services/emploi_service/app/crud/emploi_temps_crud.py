from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.emploi_temps import EmploiTemps
from app.schemas.emploi_temps import EmploiTempsCreate
from datetime import datetime, time
from app.models.salle import Salle
import httpx


def get_emploi(db: Session, emploi_id: int):
    return db.query(EmploiTemps).filter(EmploiTemps.id == emploi_id).first()


def get_emplois(db: Session, skip: int = 0, limit: int = 100, enseignant_id: int | None = None, groupe_id: int | None = None, date_from=None, date_to=None):
    query = db.query(EmploiTemps)
    if enseignant_id is not None:
        query = query.filter(EmploiTemps.enseignant_id == enseignant_id)
    if groupe_id is not None:
        query = query.filter(EmploiTemps.groupe_id == groupe_id)
    if date_from is not None:
        query = query.filter(EmploiTemps.date >= date_from)
    if date_to is not None:
        query = query.filter(EmploiTemps.date <= date_to)
    return query.offset(skip).limit(limit).all()


def _overlaps(start1: time, end1: time, start2: time, end2: time) -> bool:
    return (start1 < end2) and (start2 < end1)


def _check_conflict(db: Session, date, heure_debut, heure_fin, salle_id=None, enseignant_id=None, groupe_id=None):
    # Basic conflict checks for same date: overlapping times for same salle, enseignant or groupe
    query = db.query(EmploiTemps).filter(EmploiTemps.date == date)
    if salle_id:
        query = query.filter(EmploiTemps.salle_id == salle_id)
    if enseignant_id:
        query = query.filter(EmploiTemps.enseignant_id == enseignant_id)
    if groupe_id:
        query = query.filter(EmploiTemps.groupe_id == groupe_id)
    for existing in query.all():
        if _overlaps(existing.heure_debut, existing.heure_fin, heure_debut, heure_fin):
            return existing
    return None


def create_emploi(db: Session, emploi: EmploiTempsCreate):
    # Ensure the salle exists in the local emploi DB. If frontend sent a referentiel salle id
    # that doesn't exist here, try to fetch it from referentiel_service and insert it locally.
    if emploi.salle_id is not None:
        local_salle = db.query(Salle).filter(Salle.id == emploi.salle_id).first()
        if not local_salle:
            # attempt to fetch salle from referentiel service and create locally
            try:
                with httpx.Client(timeout=5.0) as client:
                    resp = client.get(f"http://127.0.0.1:8003/salles/{emploi.salle_id}")
                    resp.raise_for_status()
                    sdata = resp.json()
                    # create local Salle entry
                    new_s = Salle(code=sdata.get('code') or str(sdata.get('id')), type=sdata.get('type','unknown'), capacite=sdata.get('capacite') or 0)
                    db.add(new_s)
                    db.commit()
                    db.refresh(new_s)
                    # replace salle_id with the newly created local id
                    emploi.salle_id = new_s.id
            except Exception:
                # ignore and allow DB to raise foreign key error later with clear message
                pass

    # Check conflicts
    conflict = _check_conflict(db, emploi.date, emploi.heure_debut, emploi.heure_fin, salle_id=emploi.salle_id, enseignant_id=emploi.enseignant_id, groupe_id=emploi.groupe_id)
    if conflict:
        raise ValueError(f"Conflict with existing emploi id={conflict.id}")
    db_obj = EmploiTemps(
        date=emploi.date,
        heure_debut=emploi.heure_debut,
        heure_fin=emploi.heure_fin,
        salle_id=emploi.salle_id,
        matiere_id=emploi.matiere_id,
        groupe_id=emploi.groupe_id,
        enseignant_id=emploi.enseignant_id,
        matiere_nom=emploi.matiere_nom,
        enseignant_nom=emploi.enseignant_nom,
        groupe_nom=emploi.groupe_nom
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_emploi(db: Session, emploi_id: int):
    obj = db.query(EmploiTemps).filter(EmploiTemps.id == emploi_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj
