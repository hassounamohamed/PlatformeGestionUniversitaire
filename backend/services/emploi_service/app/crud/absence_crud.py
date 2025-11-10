from sqlalchemy.orm import Session
from app.models.absence import Absence
from app.schemas.absence import AbsenceCreate


def get_absence(db: Session, absence_id: int):
    return db.query(Absence).filter(Absence.id == absence_id).first()


def get_absences(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Absence).offset(skip).limit(limit).all()


def create_absence(db: Session, absence: AbsenceCreate):
    db_obj = Absence(etudiant_id=absence.etudiant_id, date=absence.date, motif=absence.motif)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_absence(db: Session, absence_id: int):
    obj = db.query(Absence).filter(Absence.id == absence_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj
