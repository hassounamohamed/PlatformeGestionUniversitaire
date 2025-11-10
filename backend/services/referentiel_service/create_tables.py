"""Utility script to create the database tables using SQLAlchemy models.

This prints the resolved DATABASE_URL so you can confirm which database will be
used for table creation (helps with debugging when no tables appear).
"""
from app.core.database import engine, Base
try:
    # prefer config2 if present
    from app.core.config2 import settings
except Exception:
    from app.core.config import settings


def create_all():
    print("Using DATABASE_URL:", settings.DATABASE_URL)
    print("Creating database tables...")
    # import models so they register themselves on Base.metadata
    try:
        from app.models import departement, matiere, enseignant, etudiant, salle  # noqa: F401
    except Exception:
        # best-effort: continue if models import fails, create_all will reflect what's registered
        pass

    Base.metadata.create_all(bind=engine)

    # list current tables for verification
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables in database:", tables)
    print("Done.")


if __name__ == "__main__":
    create_all()
