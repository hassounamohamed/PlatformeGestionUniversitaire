from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db, Base, engine
from ..crud.statistic_crud import create_statistic, get_statistic, list_statistics, compute_basic_aggregate
from ..schemas.statistic import StatisticCreate, StatisticRead

router = APIRouter()

# create tables in dev on import (convenience)
Base.metadata.create_all(bind=engine)

@router.post("/", response_model=StatisticRead)
def create_stat(stat: StatisticCreate, db: Session = Depends(get_db)):
    return create_statistic(db, stat)

@router.get("/", response_model=list[StatisticRead])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_statistics(db, skip=skip, limit=limit)

@router.get("/{stat_id}", response_model=StatisticRead)
def read_one(stat_id: int, db: Session = Depends(get_db)):
    s = get_statistic(db, stat_id)
    if not s:
        raise HTTPException(status_code=404, detail="Statistic not found")
    return s

@router.get("/aggregate/{name}")
def aggregate(name: str, db: Session = Depends(get_db)):
    agg = compute_basic_aggregate(db, name)
    return {"count": agg.count, "avg": float(agg.avg) if agg.avg is not None else None, "min": agg.min, "max": agg.max}
