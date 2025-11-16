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


@router.get('/department/{department_id}/stats')
def department_stats(department_id: int, db: Session = Depends(get_db)):
    """Return basic counts for a department: students, teachers, absences, rooms occupied (simple counts)."""
    # Since analytic_service may not own the domain models, try simple raw queries
    try:
        students = db.execute("SELECT COUNT(*) FROM students WHERE department_id = :d", {"d": department_id}).scalar()
    except Exception:
        students = None

    try:
        teachers = db.execute("SELECT COUNT(*) FROM teachers WHERE department_id = :d", {"d": department_id}).scalar()
    except Exception:
        teachers = None

    try:
        absences = db.execute("SELECT COUNT(*) FROM absences a JOIN courses c ON a.course_id = c.id WHERE c.department_id = :d", {"d": department_id}).scalar()
    except Exception:
        absences = None

    try:
        rooms = db.execute("SELECT COUNT(DISTINCT room_id) FROM emplois WHERE department_id = :d", {"d": department_id}).scalar()
    except Exception:
        rooms = None

    return {
        "department_id": department_id,
        "students": int(students) if students is not None else None,
        "teachers": int(teachers) if teachers is not None else None,
        "absences": int(absences) if absences is not None else None,
        "rooms_used": int(rooms) if rooms is not None else None,
    }
