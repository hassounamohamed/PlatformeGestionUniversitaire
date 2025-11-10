from app.core.database import engine, Base


def create_all():
    print("Creating tables for emploi_service...")
    # import models so they register
    try:
        from app.models import salle, emploi_temps, absence  # noqa: F401
    except Exception:
        pass
    Base.metadata.create_all(bind=engine)
    print("Done.")


if __name__ == '__main__':
    create_all()
