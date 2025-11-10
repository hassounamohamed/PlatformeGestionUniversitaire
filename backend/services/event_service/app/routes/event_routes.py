from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db, Base, engine
from ..crud.event_crud import create_event, get_event, list_events, update_event, delete_event
from ..schemas.event import EventCreate, EventRead

router = APIRouter()


try:
    from ..models import event as _  
except Exception:
    pass
Base.metadata.create_all(bind=engine)

@router.post("/", response_model=EventRead)
def create(ev: EventCreate, db: Session = Depends(get_db)):
    return create_event(db, ev)

@router.get("/", response_model=list[EventRead])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_events(db, skip=skip, limit=limit)

@router.get("/{ev_id}", response_model=EventRead)
def read_one(ev_id: int, db: Session = Depends(get_db)):
    e = get_event(db, ev_id)
    if not e:
        raise HTTPException(status_code=404, detail="Event not found")
    return e

@router.put("/{ev_id}", response_model=EventRead)
def put(ev_id: int, ev: EventCreate, db: Session = Depends(get_db)):
    obj = update_event(db, ev_id, ev)
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")
    return obj

@router.delete("/{ev_id}")
def delete(ev_id: int, db: Session = Depends(get_db)):
    ok = delete_event(db, ev_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"deleted": True}
