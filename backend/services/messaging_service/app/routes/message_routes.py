from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db, Base, engine
from ..crud.message_crud import create_message, get_message, list_messages, delete_message
from ..schemas.message import MessageCreate, MessageRead

router = APIRouter()

# Ensure tables exist when module imported in dev (optional)
Base.metadata.create_all(bind=engine)

@router.post("/", response_model=MessageRead)
def create(msg: MessageCreate, db: Session = Depends(get_db)):
    db_msg = create_message(db, msg)
    return db_msg


@router.get("/", response_model=list[MessageRead])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_messages(db, skip=skip, limit=limit)


@router.get("/{message_id}", response_model=MessageRead)
def read_one(message_id: int, db: Session = Depends(get_db)):
    m = get_message(db, message_id)
    if not m:
        raise HTTPException(status_code=404, detail="Message not found")
    return m


@router.delete("/{message_id}")
def delete(message_id: int, db: Session = Depends(get_db)):
    ok = delete_message(db, message_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"deleted": True}
