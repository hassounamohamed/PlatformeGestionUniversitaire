# -*- coding: utf-8 -*-
"""
Script de migration pour ajouter les colonnes de texte à emploi_temps
"""
import sys
import os
SERVICE_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SERVICE_ROOT)

from app.core.database import engine
from sqlalchemy import text, inspect

def check_and_add_columns():
    """Vérifie et ajoute les colonnes manquantes."""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('emploi_temps')]
    
    with engine.connect() as conn:
        # Check matiere_nom
        if 'matiere_nom' not in columns:
            conn.execute(text("ALTER TABLE emploi_temps ADD COLUMN matiere_nom VARCHAR"))
            conn.commit()
            print("✅ Colonne matiere_nom ajoutée")
        else:
            print("✓ Colonne matiere_nom existe déjà")
        
        # Check enseignant_nom
        if 'enseignant_nom' not in columns:
            conn.execute(text("ALTER TABLE emploi_temps ADD COLUMN enseignant_nom VARCHAR"))
            conn.commit()
            print("✅ Colonne enseignant_nom ajoutée")
        else:
            print("✓ Colonne enseignant_nom existe déjà")
        
        # Check groupe_nom
        if 'groupe_nom' not in columns:
            conn.execute(text("ALTER TABLE emploi_temps ADD COLUMN groupe_nom VARCHAR"))
            conn.commit()
            print("✅ Colonne groupe_nom ajoutée")
        else:
            print("✓ Colonne groupe_nom existe déjà")
    
    print("\n🎉 Migration terminée!")

if __name__ == "__main__":
    check_and_add_columns()
