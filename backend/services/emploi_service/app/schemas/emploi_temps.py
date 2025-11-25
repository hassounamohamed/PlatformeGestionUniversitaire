from pydantic import BaseModel
from datetime import date, time


class EmploiTempsBase(BaseModel):
    date: date
    heure_debut: time
    heure_fin: time
    salle_id: int
    matiere_id: int | None = None
    groupe_id: int | None = None
    enseignant_id: int | None = None
    matiere_nom: str | None = None
    enseignant_nom: str | None = None
    groupe_nom: str | None = None


class EmploiTempsCreate(EmploiTempsBase):
    pass


class EmploiTempsRead(EmploiTempsBase):
    id: int

    model_config = {"from_attributes": True}
