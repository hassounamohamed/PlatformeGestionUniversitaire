from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.emploi_temps import EmploiTemps
from app.schemas.emploi_temps import EmploiTempsCreate
from datetime import datetime, time


def get_emploi(db: Session, emploi_id: int):
    return db.query(EmploiTemps).filter(EmploiTemps.id == emploi_id).first()


def get_emplois(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EmploiTemps).offset(skip).limit(limit).all()


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
    # Check conflicts
    conflict = _check_conflict(db, emploi.date, emploi.heure_debut, emploi.heure_fin, salle_id=emploi.salle_id, enseignant_id=emploi.enseignant_id, groupe_id=emploi.groupe_id)
    if conflict:
        raise ValueError(f"Conflict with existing emploi id={conflict.id}")
    db_obj = EmploiTemps(date=emploi.date, heure_debut=emploi.heure_debut, heure_fin=emploi.heure_fin, salle_id=emploi.salle_id, matiere_id=emploi.matiere_id, groupe_id=emploi.groupe_id, enseignant_id=emploi.enseignant_id)
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
