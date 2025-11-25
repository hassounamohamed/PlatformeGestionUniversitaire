"""
Script pour créer les tables Niveau et Groupe dans referentiel_db
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost/referentiel_db"

async def main():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            print("🚀 Création des tables...")
            
            await session.execute(text("""
                CREATE TABLE IF NOT EXISTS niveaux (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(100) NOT NULL UNIQUE,
                    departement_id INTEGER REFERENCES departements(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            await session.execute(text("""
                CREATE TABLE IF NOT EXISTS groupes (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(100) NOT NULL UNIQUE,
                    niveau_id INTEGER REFERENCES niveaux(id),
                    departement_id INTEGER REFERENCES departements(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            await session.commit()
            print("✅ Tables créées\n")
            
            result = await session.execute(text("SELECT id FROM departements WHERE code = 'INFO'"))
            dept = result.fetchone()
            
            if dept:
                dept_id = dept[0]
                
                niveaux = [('TI1', dept_id), ('DSI2', dept_id), ('RSI2', dept_id), ('DSI3', dept_id), ('RSI3', dept_id)]
                
                for nom, did in niveaux:
                    await session.execute(
                        text("INSERT INTO niveaux (nom, departement_id) VALUES (:nom, :d) ON CONFLICT (nom) DO NOTHING"),
                        {"nom": nom, "d": did}
                    )
                
                await session.commit()
                print(f"✅ {len(niveaux)} niveaux créés\n")
                
                result = await session.execute(text("SELECT id, nom FROM niveaux"))
                niveaux_map = {r[1]: r[0] for r in result.fetchall()}
                
                groupes = [
                    ('TI11','TI1'),('TI12','TI1'),('TI13','TI1'),('TI14','TI1'),
                    ('TI15','TI1'),('TI16','TI1'),('TI17','TI1'),('TI18','TI1'),
                    ('DSI21','DSI2'),('DSI22','DSI2'),('DSI23','DSI2'),
                    ('RSI21','RSI2'),('DSI31','DSI3'),('DSI32','DSI3'),('RSI31','RSI3')
                ]
                
                for g, n in groupes:
                    nid = niveaux_map.get(n)
                    if nid:
                        await session.execute(
                            text("INSERT INTO groupes (nom, niveau_id, departement_id) VALUES (:g, :n, :d) ON CONFLICT (nom) DO NOTHING"),
                            {"g": g, "n": nid, "d": dept_id}
                        )
                
                await session.commit()
                print(f"✅ {len(groupes)} groupes créés\n")
                
                r1 = await session.execute(text("SELECT COUNT(*) FROM niveaux"))
                r2 = await session.execute(text("SELECT COUNT(*) FROM groupes"))
                print(f"📊 Niveaux: {r1.scalar()}, Groupes: {r2.scalar()}")
                print("🎉 Terminé!")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            await session.rollback()
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
