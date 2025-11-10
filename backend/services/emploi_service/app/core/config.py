from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:mohamed123@localhost:5432/emploi_db"
    model_config = {"env_file": ".env"}


settings = Settings()
