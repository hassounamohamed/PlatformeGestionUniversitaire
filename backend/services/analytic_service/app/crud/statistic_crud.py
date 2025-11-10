from sqlalchemy.orm import Session
from ..models.statistic import Statistic
from ..schemas.statistic import StatisticCreate
from sqlalchemy import func


def create_statistic(db: Session, stat: StatisticCreate) -> Statistic:
    db_obj = Statistic(name=stat.name, value=stat.value, details=stat.details)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_statistic(db: Session, stat_id: int):
    return db.query(Statistic).filter(Statistic.id == stat_id).first()


def list_statistics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Statistic).order_by(Statistic.created_at.desc()).offset(skip).limit(limit).all()


def compute_basic_aggregate(db: Session, name: str):
    # Returns count, avg, min, max for a given metric name
    q = db.query(
        func.count(Statistic.id).label("count"),
        func.avg(Statistic.value).label("avg"),
        func.min(Statistic.value).label("min"),
        func.max(Statistic.value).label("max"),
    ).filter(Statistic.name == name)
    return q.one()  # tuple-like with named fields
