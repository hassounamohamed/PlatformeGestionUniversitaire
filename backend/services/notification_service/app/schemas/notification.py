from pydantic import BaseModel, EmailStr
from datetime import datetime


class NotificationBase(BaseModel):
    to: EmailStr
    subject: str
    body: str
    type: str | None = "email"


class NotificationCreate(NotificationBase):
    pass


class NotificationRead(NotificationBase):
    id: int
    status: str
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
