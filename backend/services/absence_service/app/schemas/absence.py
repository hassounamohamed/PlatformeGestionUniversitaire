from pydantic import BaseModel


class AbsenceBase(BaseModel):
    etudiant_id: int
    emploi_id: int | None = None
    motif: str | None = None
    statut: str | None = None


class AbsenceCreate(AbsenceBase):
    pass


class AbsenceRead(AbsenceBase):
    id: int

    model_config = {"from_attributes": True}
