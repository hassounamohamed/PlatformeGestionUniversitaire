from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.notification import NotificationCreate, NotificationRead
from app.crud.notification_crud import get_notification, get_notifications
from app.core.database import get_db
from app.services.notification_service import send_notification

router = APIRouter()


@router.get("/", response_model=List[NotificationRead])
def list_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_notifications(db, skip=skip, limit=limit)


@router.post("/", response_model=NotificationRead)
def create_notification_endpoint(background_tasks: BackgroundTasks, payload: NotificationCreate, db: Session = Depends(get_db)):
    try:
        return send_notification(background_tasks, db, payload)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get("/{notification_id}", response_model=NotificationRead)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    obj = get_notification(db, notification_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Notification not found")
    return obj
