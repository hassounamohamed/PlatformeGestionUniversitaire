"""
Script Python pour appliquer la migration et ajouter les colonnes manquantes
"""
from sqlalchemy import create_engine, text

# Configuration de la connexion
DATABASE_URL = "postgresql://postgres:password@localhost:5432/emploi_db"
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Ajouter matiere_nom
        try:
            conn.execute(text("ALTER TABLE emploi_temps ADD COLUMN matiere_nom VARCHAR;"))
            conn.commit()
            print("✅ Colonne matiere_nom ajoutée")
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e).lower():
                print("✓ Colonne matiere_nom existe déjà")
            else:
                print(f"Erreur matiere_nom: {e}")
        
        # Ajouter enseignant_nom
        try:
            conn.execute(text("ALTER TABLE emploi_temps ADD COLUMN enseignant_nom VARCHAR;"))
            conn.commit()
            print("✅ Colonne enseignant_nom ajoutée")
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e).lower():
                print("✓ Colonne enseignant_nom existe déjà")
            else:
                print(f"Erreur enseignant_nom: {e}")
        
        # Ajouter groupe_nom
        try:
            conn.execute(text("ALTER TABLE emploi_temps ADD COLUMN groupe_nom VARCHAR;"))
            conn.commit()
            print("✅ Colonne groupe_nom ajoutée")
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e).lower():
                print("✓ Colonne groupe_nom existe déjà")
            else:
                print(f"Erreur groupe_nom: {e}")
    
    print("\n🎉 Migration terminée avec succès!")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
