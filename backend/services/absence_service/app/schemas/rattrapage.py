from pydantic import BaseModel
from datetime import date, time


class RattrapageBase(BaseModel):
    absence_id: int
    date: date
    heure_debut: time
    heure_fin: time
    salle_id: int | None = None


class RattrapageCreate(RattrapageBase):
    pass


class RattrapageRead(RattrapageBase):
    id: int

    model_config = {"from_attributes": True}
