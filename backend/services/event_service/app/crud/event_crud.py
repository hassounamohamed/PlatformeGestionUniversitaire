from sqlalchemy.orm import Session
from ..models.event import Event
from ..schemas.event import EventCreate


def create_event(db: Session, ev: EventCreate) -> Event:
    db_ev = Event(
        titre=ev.titre,
        type=ev.type,
        date=ev.date,
        description=ev.description,
    )
    db.add(db_ev)
    db.commit()
    db.refresh(db_ev)
    return db_ev


def get_event(db: Session, ev_id: int) -> Event | None:
    return db.query(Event).filter(Event.id == ev_id).first()


def list_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Event).order_by(Event.date.desc()).offset(skip).limit(limit).all()


def update_event(db: Session, ev_id: int, ev: EventCreate) -> Event | None:
    obj = db.query(Event).filter(Event.id == ev_id).first()
    if not obj:
        return None
    obj.titre = ev.titre
    obj.type = ev.type
    obj.date = ev.date
    obj.description = ev.description
    db.commit()
    db.refresh(obj)
    return obj


def delete_event(db: Session, ev_id: int) -> bool:
    obj = db.query(Event).filter(Event.id == ev_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
