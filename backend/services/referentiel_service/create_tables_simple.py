"""
Script simple pour créer les tables niveaux et groupes
"""
from sqlalchemy import create_engine, text

# Connexion directe
DATABASE_URL = "postgresql+psycopg2://postgres:mohamed123@localhost:5432/referentiel_db"
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Créer la table niveaux
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS niveaux (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(100) NOT NULL UNIQUE,
            departement_id INTEGER REFERENCES departements(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    
    # Créer la table groupes
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
    
    # Vérifier si le département Informatique existe
    result = conn.execute(text("SELECT id FROM departements WHERE nom = 'Informatique'"))
    dept = result.fetchone()
    
    if not dept:
        # Créer le département Informatique
        conn.execute(text("INSERT INTO departements (nom) VALUES ('Informatique')"))
        conn.commit()
        result = conn.execute(text("SELECT id FROM departements WHERE nom = 'Informatique'"))
        dept = result.fetchone()
    
    dept_id = dept[0]
    print(f"Département Informatique trouvé: ID={dept_id}")
    
    # Insérer les niveaux
    niveaux = [
        ('TI1', dept_id),
        ('DSI2', dept_id),
        ('RSI2', dept_id),
        ('DSI3', dept_id),
        ('RSI3', dept_id)
    ]
    
    for nom, did in niveaux:
        conn.execute(
            text("INSERT INTO niveaux (nom, departement_id) VALUES (:nom, :d) ON CONFLICT (nom) DO NOTHING"),
            {"nom": nom, "d": did}
        )
    
    conn.commit()
    print("Niveaux insérés")
    
    # Récupérer les IDs des niveaux
    result = conn.execute(text("SELECT id, nom FROM niveaux"))
    niveaux_map = {r[1]: r[0] for r in result.fetchall()}
    print(f"Niveaux créés: {list(niveaux_map.keys())}")
    
    # Insérer les groupes
    groupes = [
        ('TI11', 'TI1'), ('TI12', 'TI1'), ('TI13', 'TI1'), ('TI14', 'TI1'),
        ('TI15', 'TI1'), ('TI16', 'TI1'), ('TI17', 'TI1'), ('TI18', 'TI1'),
        ('DSI21', 'DSI2'), ('DSI22', 'DSI2'), ('DSI23', 'DSI2'),
        ('RSI21', 'RSI2'),
        ('DSI31', 'DSI3'), ('DSI32', 'DSI3'),
        ('RSI31', 'RSI3')
    ]
    
    for g, n in groupes:
        nid = niveaux_map.get(n)
        if nid:
            conn.execute(
                text("INSERT INTO groupes (nom, niveau_id, departement_id) VALUES (:g, :n, :d) ON CONFLICT (nom) DO NOTHING"),
                {"g": g, "n": nid, "d": dept_id}
            )
    
    conn.commit()
    print("Groupes insérés")
    
    # Compter les résultats
    r1 = conn.execute(text("SELECT COUNT(*) FROM niveaux"))
    r2 = conn.execute(text("SELECT COUNT(*) FROM groupes"))
    
    print(f"\n✅ Succès!")
    print(f"   - Niveaux: {r1.scalar()}")
    print(f"   - Groupes: {r2.scalar()}")
