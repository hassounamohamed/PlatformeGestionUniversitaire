import csv
import io
from typing import List
from sqlalchemy.orm import Session
from ..crud.statistic_crud import list_statistics


def export_statistics_csv(db: Session, skip: int = 0, limit: int = 100) -> bytes:
    rows = list_statistics(db, skip=skip, limit=limit)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "value", "details", "created_at"])
    for r in rows:
        writer.writerow([r.id, r.name, r.value, r.details, r.created_at.isoformat()])
    return output.getvalue().encode("utf-8")


