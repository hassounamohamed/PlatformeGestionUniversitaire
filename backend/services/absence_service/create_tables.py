from app.core.database import engine, Base


def create_all():
    print("Creating tables for absence_service...")
    try:
        from app.models import absence, rattrapage, justificatif  # noqa: F401
    except Exception:
        pass
    Base.metadata.create_all(bind=engine)
    print("Done.")


if __name__ == '__main__':
    create_all()
