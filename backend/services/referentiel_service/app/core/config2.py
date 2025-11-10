from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:mohamed123@localhost:5432/referentiel_db"
    # Simple admin API key used by internal admin endpoints. Set in .env (e.g. ADMIN_API_KEY=changeme)
    ADMIN_API_KEY: str = ""

    model_config = {"env_file": ".env"}


settings = Settings()
