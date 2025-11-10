from sqlalchemy.orm import Session
from app.models.rattrapage import Rattrapage
from app.schemas.rattrapage import RattrapageCreate


def get_rattrapage(db: Session, r_id: int):
    return db.query(Rattrapage).filter(Rattrapage.id == r_id).first()


def get_rattrapages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Rattrapage).offset(skip).limit(limit).all()


def create_rattrapage(db: Session, r: RattrapageCreate):
    db_obj = Rattrapage(absence_id=r.absence_id, date=r.date, heure_debut=r.heure_debut, heure_fin=r.heure_fin, salle_id=r.salle_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_rattrapage(db: Session, r_id: int):
    obj = db.query(Rattrapage).filter(Rattrapage.id == r_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj
