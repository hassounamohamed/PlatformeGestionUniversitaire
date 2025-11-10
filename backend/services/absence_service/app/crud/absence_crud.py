from sqlalchemy.orm import Session
from app.models.absence import Absence
from app.schemas.absence import AbsenceCreate


def get_absence(db: Session, absence_id: int):
    return db.query(Absence).filter(Absence.id == absence_id).first()


def get_absences(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Absence).offset(skip).limit(limit).all()


def create_absence(db: Session, absence: AbsenceCreate):
    db_obj = Absence(etudiant_id=absence.etudiant_id, emploi_id=absence.emploi_id, motif=absence.motif, statut=absence.statut or "pending")
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_absence(db: Session, absence_id: int, patch: dict):
    obj = db.query(Absence).filter(Absence.id == absence_id).first()
    if not obj:
        return None
    for k, v in patch.items():
        if hasattr(obj, k) and v is not None:
            setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_absence(db: Session, absence_id: int):
    obj = db.query(Absence).filter(Absence.id == absence_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj
