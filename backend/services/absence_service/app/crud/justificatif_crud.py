from sqlalchemy.orm import Session
from app.models.justificatif import Justificatif
from app.schemas.justificatif import JustificatifCreate


def get_justificatif(db: Session, j_id: int):
    return db.query(Justificatif).filter(Justificatif.id == j_id).first()


def get_justificatifs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Justificatif).offset(skip).limit(limit).all()


def create_justificatif(db: Session, j: JustificatifCreate):
    db_obj = Justificatif(absence_id=j.absence_id, file_path=j.file_path, statut=j.statut or "pending")
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_justificatif(db: Session, j_id: int, patch: dict):
    obj = db.query(Justificatif).filter(Justificatif.id == j_id).first()
    if not obj:
        return None
    for k, v in patch.items():
        if hasattr(obj, k) and v is not None:
            setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_justificatif(db: Session, j_id: int):
    obj = db.query(Justificatif).filter(Justificatif.id == j_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj
