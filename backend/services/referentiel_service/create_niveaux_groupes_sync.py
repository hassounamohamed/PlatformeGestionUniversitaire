"""
Script synchrone pour créer les tables Niveau et Groupe
"""
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:root@localhost:5432/referentiel_db"

def main():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            print("🚀 Création des tables...")
            
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS niveaux (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(100) NOT NULL UNIQUE,
                    departement_id INTEGER REFERENCES departements(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS groupes (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(100) NOT NULL UNIQUE,
                    niveau_id INTEGER REFERENCES niveaux(id),
                    departement_id INTEGER REFERENCES departements(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            conn.commit()
            print("✅ Tables créées\n")
            
            result = conn.execute(text("SELECT id FROM departements WHERE code = 'INFO'"))
            dept = result.fetchone()
            
            if not dept:
                print("📝 Création du département Informatique...")
                conn.execute(text("INSERT INTO departements (nom, code) VALUES ('Informatique', 'INFO')"))
                conn.commit()
                result = conn.execute(text("SELECT id FROM departements WHERE code = 'INFO'"))
                dept = result.fetchone()
            
            dept_id = dept[0]
            print(f"✅ Département ID: {dept_id}\n")
            
            print("📊 Insertion des niveaux...")
            niveaux = [('TI1', dept_id), ('DSI2', dept_id), ('RSI2', dept_id), ('DSI3', dept_id), ('RSI3', dept_id)]
            
            for nom, did in niveaux:
                conn.execute(
                    text("INSERT INTO niveaux (nom, departement_id) VALUES (:nom, :d) ON CONFLICT (nom) DO NOTHING"),
                    {"nom": nom, "d": did}
                )
            
            conn.commit()
            print(f"✅ {len(niveaux)} niveaux créés\n")
            
            print("👥 Insertion des groupes...")
            result = conn.execute(text("SELECT id, nom FROM niveaux"))
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
                    conn.execute(
                        text("INSERT INTO groupes (nom, niveau_id, departement_id) VALUES (:g, :n, :d) ON CONFLICT (nom) DO NOTHING"),
                        {"g": g, "n": nid, "d": dept_id}
                    )
            
            conn.commit()
            print(f"✅ {len(groupes)} groupes créés\n")
            
            r1 = conn.execute(text("SELECT COUNT(*) FROM niveaux"))
            r2 = conn.execute(text("SELECT COUNT(*) FROM groupes"))
            print(f"📊 Total - Niveaux: {r1.scalar()}, Groupes: {r2.scalar()}")
            print("\n🎉 Terminé avec succès!")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    main()
