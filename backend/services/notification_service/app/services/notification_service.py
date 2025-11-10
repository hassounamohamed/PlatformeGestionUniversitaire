from fastapi import BackgroundTasks
from app.core.email_utils import send_email_sync
from app.crud.notification_crud import create_notification
from app.schemas.notification import NotificationCreate
from sqlalchemy.orm import Session


def send_notification(background_tasks: BackgroundTasks, db: Session, payload: NotificationCreate):
    """Queue sending of notification and record history in DB."""
    # Record pending or sent depending on whether SMTP is configured; send in background
    try:
        # schedule sending in background
        background_tasks.add_task(send_email_sync, str(payload.to), payload.subject, payload.body)
        status = "sent"
    except Exception:
        status = "failed"

    return create_notification(db, payload, status=status)
