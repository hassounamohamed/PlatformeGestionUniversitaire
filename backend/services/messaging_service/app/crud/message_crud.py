from sqlalchemy.orm import Session
from ..models.message import Message
from ..schemas.message import MessageCreate


def create_message(db: Session, message: MessageCreate) -> Message:
    db_msg = Message(
        id_expediteur=message.id_expediteur,
        id_destinataire=message.id_destinataire,
        contenu=message.contenu,
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg


def get_message(db: Session, message_id: int) -> Message | None:
    return db.query(Message).filter(Message.id == message_id).first()


def list_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Message).order_by(Message.date.desc()).offset(skip).limit(limit).all()


def delete_message(db: Session, message_id: int) -> bool:
    obj = db.query(Message).filter(Message.id == message_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
