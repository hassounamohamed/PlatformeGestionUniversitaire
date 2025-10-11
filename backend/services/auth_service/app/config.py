import os
try:
    from pydantic_settings import BaseSettings
except Exception:  # pragma: no cover - fallback for lightweight environments
    try:
        from pydantic import BaseSettings  # older pydantic packaged BaseSettings
    except Exception:
        # Minimal fallback so imports don't fail in environments without pydantic
        class BaseSettings:  # type: ignore
            def __init_subclass__(cls, **kwargs):
                return None


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:mohamed123@localhost/auth_db"
    )

    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-this-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Application
    DEBUG: bool = True

    class Config:
        case_sensitive = True


settings = Settings()