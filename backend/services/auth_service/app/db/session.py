import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from ..config import settings

# Ensure SQLAlchemy engine-level INFO logs are suppressed by default
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# Créer le moteur asynchrone
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Créer la session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

from typing import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency pour obtenir une session de base de données
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()