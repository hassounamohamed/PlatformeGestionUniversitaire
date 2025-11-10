from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Default to sqlite for quick local runs. Override with DATABASE_URL in .env for Postgres.
    DATABASE_URL: str = "postgresql+psycopg2://postgres:mohamed123@localhost:5432/analytic_db"
    SERVICE_NAME: str = "analytic_service"

    class Config:
        env_file = ".env"


settings = Settings()
