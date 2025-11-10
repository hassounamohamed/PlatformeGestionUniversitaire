from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    DATABASE_URL: str = "postgresql+psycopg2://postgres:mohamed123@localhost:5432/event_db"
    SERVICE_NAME: str = "event_service"

    class Config:
        env_file = ".env"


settings = Settings()
