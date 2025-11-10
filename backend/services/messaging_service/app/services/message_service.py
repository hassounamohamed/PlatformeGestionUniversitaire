from fastapi import BackgroundTasks
from ..crud.message_crud import create_message
from sqlalchemy.orm import Session
from ..schemas.message import MessageCreate


def send_message_and_notify(background_tasks: BackgroundTasks, db: Session, payload: MessageCreate):
    # Save message immediately
    msg = create_message(db, payload)

    # Placeholder for notification logic (push, websockets, etc.)
    # e.g., background_tasks.add_task(push_notify, msg.id)

    return msg
