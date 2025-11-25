import sys
from pathlib import Path

# Insert service folder at front of sys.path
service_dir = Path(__file__).parent
sys.path.insert(0, str(service_dir))

from app.core.database import SessionLocal
from app.models.departement import Departement
from app.models.matiere import Matiere
from app.models.enseignant import Enseignant
from app.models.salle import Salle

def insert_test_data():
    db = SessionLocal()
    try:
        # Vérifier si des données existent déjà
        dept_count = db.query(Departement).count()
        print(f"Départements existants: {dept_count}")
        
        if dept_count == 0:
            # Ajouter un département
            dept = Departement(nom="Informatique")
            db.add(dept)
            db.commit()
            db.refresh(dept)
            print(f"Département créé: {dept.nom} (ID: {dept.id})")
        else:
            dept = db.query(Departement).first()
            print(f"Utilisation du département existant: {dept.nom}")
        
        # Ajouter des enseignants
        ens_count = db.query(Enseignant).count()
        print(f"Enseignants existants: {ens_count}")
        
        if ens_count == 0:
            enseignants = [
                Enseignant(nom="Dupont", prenom="Jean", email="jean.dupont@univ.fr", departement_id=dept.id),
                Enseignant(nom="Martin", prenom="Marie", email="marie.martin@univ.fr", departement_id=dept.id),
            ]
            for ens in enseignants:
                db.add(ens)
            db.commit()
            print(f"Enseignants créés: {len(enseignants)}")
        
        # Ajouter des matières
        mat_count = db.query(Matiere).count()
        print(f"Matières existantes: {mat_count}")
        
        if mat_count == 0:
            matieres = [
                Matiere(nom="Programmation", code="INFO101"),
                Matiere(nom="Base de données", code="INFO102"),
                Matiere(nom="Réseaux", code="INFO103"),
            ]
            for mat in matieres:
                db.add(mat)
            db.commit()
            print(f"Matières créées: {len(matieres)}")
        
        # Ajouter des salles
        salle_count = db.query(Salle).count()
        print(f"Salles existantes: {salle_count}")
        
        if salle_count == 0:
            salles = [
                Salle(code="A101", type="TD", capacite=30),
                Salle(code="A102", type="Cours", capacite=50),
                Salle(code="B201", type="TP", capacite=25),
            ]
            for salle in salles:
                db.add(salle)
            db.commit()
            print(f"Salles créées: {len(salles)}")
        
        print("\n✓ Données de test insérées avec succès!")
        
    except Exception as e:
        print(f"Erreur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    insert_test_data()
