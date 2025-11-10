from sqlalchemy.orm import Session
from app.models.salle import Salle
from app.schemas.salle import SalleCreate


def get_salle(db: Session, salle_id: int):
    return db.query(Salle).filter(Salle.id == salle_id).first()


def get_salles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Salle).offset(skip).limit(limit).all()


def create_salle(db: Session, salle: SalleCreate):
    db_obj = Salle(code=salle.code, type=salle.type, capacite=salle.capacite)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_salle(db: Session, salle_id: int, code: str | None = None, type: str | None = None, capacite: int | None = None):
    obj = db.query(Salle).filter(Salle.id == salle_id).first()
    if not obj:
        return None
    if code is not None:
        obj.code = code
    if type is not None:
        obj.type = type
    if capacite is not None:
        obj.capacite = capacite
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_salle(db: Session, salle_id: int):
    obj = db.query(Salle).filter(Salle.id == salle_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj
