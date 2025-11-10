from pydantic import BaseModel
from datetime import date


class AbsenceBase(BaseModel):
    etudiant_id: int
    date: date
    motif: str | None = None


class AbsenceCreate(AbsenceBase):
    pass


class AbsenceRead(AbsenceBase):
    id: int

    model_config = {"from_attributes": True}
