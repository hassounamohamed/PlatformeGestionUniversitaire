"""Create DB tables for analytic_service (dev helper)."""
from app.core.database import engine, Base


def main():
    print("Creating tables for analytic_service...")
    # Import models so they register on Base.metadata
    try:
        from app.models import statistic  # noqa: F401
    except Exception:
        pass
    Base.metadata.create_all(bind=engine)
    print("Done.")


if __name__ == "__main__":
    main()
