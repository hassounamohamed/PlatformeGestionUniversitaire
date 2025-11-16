from .session import engine, Base
import logging

# Importer tous les modèles pour que Base les connaisse
from ..models.user import User  # noqa: F401

logger = logging.getLogger(__name__)


async def init_db(): 
    """
    Initialise la base de données en créant toutes les tables
    """
    try:
        async with engine.begin() as conn:
            # Créer toutes les tables
            await conn.run_sync(Base.metadata.create_all)

        logger.info("✅ Base de données initialisée avec succès")

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
        raise


async def drop_db():
    """
    Supprime toutes les tables (utile pour les tests)
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        logger.info("✅ Base de données supprimée avec succès")

    except Exception as e:
        logger.error(f"❌ Erreur lors de la suppression de la base de données: {e}")
        raise


if __name__ == "__main__":
    import asyncio

    asyncio.run(init_db())