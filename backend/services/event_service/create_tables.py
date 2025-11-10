"""Create DB tables for event_service (dev helper)."""
from app.core.database import engine, Base


def main():
    print("Creating tables for event_service...")
    # import models so they register on Base.metadata
    try:
        from app.models import event  # noqa: F401
    except Exception:
        pass
    Base.metadata.create_all(bind=engine)
    print("Done.")


if __name__ == "__main__":
    main()
