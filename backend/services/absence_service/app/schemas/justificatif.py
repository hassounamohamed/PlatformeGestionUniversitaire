from pydantic import BaseModel
from datetime import datetime


class JustificatifBase(BaseModel):
    absence_id: int
    file_path: str | None = None
    statut: str | None = None


class JustificatifCreate(JustificatifBase):
    pass


class JustificatifRead(JustificatifBase):
    id: int
    uploaded_at: datetime | None = None

    model_config = {"from_attributes": True}
