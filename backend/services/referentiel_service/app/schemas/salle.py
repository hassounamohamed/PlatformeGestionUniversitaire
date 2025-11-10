from pydantic import BaseModel


class SalleBase(BaseModel):
    code: str
    type: str
    capacite: int


class SalleCreate(SalleBase):
    pass


class SalleRead(SalleBase):
    id: int

    model_config = {"from_attributes": True}
