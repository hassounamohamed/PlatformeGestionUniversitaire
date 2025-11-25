"""
Route pour créer les tables niveaux et groupes
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.post("/setup/create-niveaux-groupes")
def create_niveaux_groupes(db: Session = Depends(get_db)):
    """Crée les tables niveaux et groupes et insère les données"""
    try:
        # Créer la table niveaux
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS niveaux (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(100) NOT NULL UNIQUE,
                departement_id INTEGER REFERENCES departements(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Créer la table groupes
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS groupes (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(100) NOT NULL UNIQUE,
                niveau_id INTEGER REFERENCES niveaux(id),
                departement_id INTEGER REFERENCES departements(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        db.commit()
        
        # Vérifier si le département Informatique existe
        result = db.execute(text("SELECT id FROM departements WHERE code = 'INFO'"))
        dept = result.fetchone()
        
        if not dept:
            # Créer le département Informatique
            db.execute(text("INSERT INTO departements (nom, code) VALUES ('Informatique', 'INFO')"))
            db.commit()
            result = db.execute(text("SELECT id FROM departements WHERE code = 'INFO'"))
            dept = result.fetchone()
        
        dept_id = dept[0]
        
        # Insérer les niveaux
        niveaux = [
            ('TI1', dept_id),
            ('DSI2', dept_id),
            ('RSI2', dept_id),
            ('DSI3', dept_id),
            ('RSI3', dept_id)
        ]
        
        for nom, did in niveaux:
            db.execute(
                text("INSERT INTO niveaux (nom, departement_id) VALUES (:nom, :d) ON CONFLICT (nom) DO NOTHING"),
                {"nom": nom, "d": did}
            )
        
        db.commit()
        
        # Récupérer les IDs des niveaux
        result = db.execute(text("SELECT id, nom FROM niveaux"))
        niveaux_map = {r[1]: r[0] for r in result.fetchall()}
        
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
                db.execute(
                    text("INSERT INTO groupes (nom, niveau_id, departement_id) VALUES (:g, :n, :d) ON CONFLICT (nom) DO NOTHING"),
                    {"g": g, "n": nid, "d": dept_id}
                )
        
        db.commit()
        
        # Compter les résultats
        r1 = db.execute(text("SELECT COUNT(*) FROM niveaux"))
        r2 = db.execute(text("SELECT COUNT(*) FROM groupes"))
        
        return {
            "status": "success",
            "message": "Tables créées et données insérées",
            "niveaux_count": r1.scalar(),
            "groupes_count": r2.scalar()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
