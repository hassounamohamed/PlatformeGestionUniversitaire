from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate


def create_notification(db: Session, n: NotificationCreate, status: str = "sent"):
    db_obj = Notification(to=str(n.to), subject=n.subject, body=n.body, type=n.type or "email", status=status)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_notification(db: Session, notification_id: int):
    return db.query(Notification).filter(Notification.id == notification_id).first()


def get_notifications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Notification).offset(skip).limit(limit).all()
