from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database configuration (PostgreSQL)
    DATABASE_URL: str = "postgresql+psycopg2://postgres:mohamed123@localhost:5432/notification_db"

    # SMTP settings for sending emails
    SMTP_HOST: str = "smtp.gmail.com"        # Exemple : Gmail SMTP server
    SMTP_PORT: int = 587
    SMTP_USER: str = "votre.email@gmail.com"  # Remplace par ton email
    SMTP_PASSWORD: str = "mot_de_passe_app"   # Mot de passe d’application Gmail
    SMTP_FROM: str = "no-reply@example.com"   # Adresse d’expéditeur par défaut

    # Configuration pour le chargement depuis le fichier .env
    class Config:
        env_file = ".env"  # Charger les variables d'environnement depuis .env


# Initialize settings instance
settings = Settings()
