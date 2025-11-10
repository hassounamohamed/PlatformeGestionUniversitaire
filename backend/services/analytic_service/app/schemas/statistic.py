from pydantic import BaseModel, ConfigDict
from datetime import datetime


class StatisticCreate(BaseModel):
    name: str
    value: float
    details: str | None = None


class StatisticRead(StatisticCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
