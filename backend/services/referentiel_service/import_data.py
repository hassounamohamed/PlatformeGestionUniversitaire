"""
Script d'importation des données de référence (enseignants, matières, salles)
pour le département informatique.
"""
import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Ajouter le répertoire du service au path
SERVICE_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SERVICE_ROOT)

from app.core.database import Base
from app.models.enseignant import Enseignant
from app.models.matiere import Matiere
from app.models.salle import Salle
from app.models.departement import Departement

# Connexion à la base de données
DATABASE_URL = "postgresql://postgres:root@localhost:5432/referentiel_db"
engine = create_engine(DATABASE_URL, client_encoding='utf8')
Base.metadata.create_all(bind=engine)

# Données à importer
ENSEIGNANTS_DATA = [
    # TI14
    {"nom": "Jemli", "prenom": "Sarra", "email": "sarra.jemli@iset.tn"},
    {"nom": "Zarroug", "prenom": "Wafa", "email": "wafa.zarroug@iset.tn"},
    {"nom": "Najjari", "prenom": "Houda", "email": "houda.najjari@iset.tn"},
    {"nom": "Ghaouar", "prenom": "Yousra", "email": "yousra.ghaouar@iset.tn"},
    {"nom": "Salah", "prenom": "Daoud", "email": "daoud.salah@iset.tn"},
    {"nom": "Chrait", "prenom": "Ibrahim", "email": "ibrahim.chrait@iset.tn"},
    {"nom": "Touati", "prenom": "Fadwa", "email": "fadwa.touati@iset.tn"},
    {"nom": "Ben Youssef", "prenom": "Taher", "email": "taher.benyoussef@iset.tn"},
    {"nom": "Baccari", "prenom": "Taheya", "email": "taheya.baccari@iset.tn"},
    {"nom": "Sfaya", "prenom": "Taha", "email": "taha.sfaya@iset.tn"},
    # Autres
    {"nom": "Mbarki", "prenom": "Mohamed", "email": "mohamed.mbarki@iset.tn"},
    {"nom": "B.M", "prenom": "Soufiene", "email": "soufiene.bm@iset.tn"},
    {"nom": "Hadfi", "prenom": "Ebtihal", "email": "ebtihal.hadfi@iset.tn"},
    {"nom": "Touati", "prenom": "Haifa", "email": "haifa.touati@iset.tn"},
    {"nom": "Chraigui", "prenom": "Bilel", "email": "bilel.chraigui@iset.tn"},
    {"nom": "Arfaoui", "prenom": "Dzirya", "email": "dzirya.arfaoui@iset.tn"},
    {"nom": "Hafsi", "prenom": "Haithem", "email": "haithem.hafsi@iset.tn"},
    {"nom": "Dguechi", "prenom": "Haifa", "email": "haifa.dguechi@iset.tn"},
    {"nom": "Benneji", "prenom": "Hamed", "email": "hamed.benneji@iset.tn"},
    {"nom": "Jeridi", "prenom": "Mariem", "email": "mariem.jeridi@iset.tn"},
    {"nom": "Chetoui", "prenom": "Ibtikhar", "email": "ibtikhar.chetoui@iset.tn"},
    {"nom": "Omrani", "prenom": "Takwa", "email": "takwa.omrani@iset.tn"},
    {"nom": "Hedfi", "prenom": "Ebtihal", "email": "ebtihal.hedfi@iset.tn"},
]

MATIERES_DATA = [
    # TI14
    "Développement Web et Multimédia I",
    "Atelier Développement Web et Multimédia I",
    "Atelier Programmation",
    "Atelier Mathématiques",
    "Atelier Systèmes Logiques",
    "Business Culture",
    "Architecture des Ordinateurs",
    "English for Computing 1",
    "Algorithmique & Programmation 1",
    "Bureautique",
    "Mathématique Appliquée",
    "Technique d'expression 1",
    "2CN",
    # Autres
    "Administration Systèmes",
    "LPIC1",
    "Communication en entreprise",
    "Bases de Données",
    "Atelier Bases de Données",
    "Atelier Programmation Objet",
    "Réseaux Locaux & TCP/IP",
    "Droit de l'Informatique & Propriétés",
    "High Tech English",
    "Cybersecurity Essentials",
    "Programmation Objet",
    "Modélisation Objet (UML2)",
    "Outils de Développement Collaboratif",
    "Programmation Python Avancée",
    "Atelier Développement Web côté Serveur",
    "Atelier Framework côté Client",
    "Atelier Base de Données",
]

SALLES_DATA = [
    {"code": "LI 03", "type": "Laboratoire", "capacite": 30},
    {"code": "LI 04", "type": "Laboratoire", "capacite": 30},
    {"code": "LI 05", "type": "Laboratoire", "capacite": 30},
    {"code": "LI 06", "type": "Laboratoire", "capacite": 30},
    {"code": "LI 07", "type": "Laboratoire", "capacite": 30},
    {"code": "LG 01", "type": "Laboratoire", "capacite": 30},
    {"code": "LG 04", "type": "Laboratoire", "capacite": 30},
    {"code": "SI 01", "type": "Salle", "capacite": 40},
    {"code": "SI 03", "type": "Salle", "capacite": 40},
    {"code": "SI 04", "type": "Salle", "capacite": 40},
    {"code": "SI 09", "type": "Salle", "capacite": 40},
    {"code": "AMPHI", "type": "Amphithéâtre", "capacite": 100},
]


def import_data():
    """Importe les données de référence dans la base de données."""
    db = Session(bind=engine)
    
    try:
        # 1. Créer le département informatique s'il n'existe pas
        dept = db.query(Departement).filter(Departement.nom == "Informatique").first()
        if not dept:
            dept = Departement(nom="Informatique", code="INFO")
            db.add(dept)
            db.commit()
            db.refresh(dept)
            print(f"✅ Département créé: {dept.nom}")
        else:
            print(f"✓ Département existe déjà: {dept.nom}")

        # 2. Importer les enseignants (éviter les doublons)
        enseignants_created = 0
        for data in ENSEIGNANTS_DATA:
            existing = db.query(Enseignant).filter(Enseignant.email == data["email"]).first()
            if not existing:
                enseignant = Enseignant(
                    nom=data["nom"],
                    prenom=data["prenom"],
                    email=data["email"],
                    departement_id=dept.id
                )
                db.add(enseignant)
                enseignants_created += 1
        
        db.commit()
        print(f"✅ {enseignants_created} enseignants créés (doublons ignorés)")

        # 3. Importer les matières (éviter les doublons)
        matieres_created = 0
        for nom_matiere in MATIERES_DATA:
            existing = db.query(Matiere).filter(Matiere.nom == nom_matiere).first()
            if not existing:
                matiere = Matiere(
                    nom=nom_matiere,
                    departement_id=dept.id
                )
                db.add(matiere)
                matieres_created += 1
        
        db.commit()
        print(f"✅ {matieres_created} matières créées (doublons ignorées)")

        # 4. Importer les salles (éviter les doublons)
        salles_created = 0
        for data in SALLES_DATA:
            existing = db.query(Salle).filter(Salle.code == data["code"]).first()
            if not existing:
                salle = Salle(
                    code=data["code"],
                    type=data["type"],
                    capacite=data["capacite"]
                )
                db.add(salle)
                salles_created += 1
        
        db.commit()
        print(f"✅ {salles_created} salles créées (doublons ignorés)")

        print("\n🎉 Importation terminée avec succès!")
        
        # Afficher les statistiques
        total_enseignants = db.query(Enseignant).count()
        total_matieres = db.query(Matiere).count()
        total_salles = db.query(Salle).count()
        
        print(f"\n📊 Statistiques:")
        print(f"   - Enseignants: {total_enseignants}")
        print(f"   - Matières: {total_matieres}")
        print(f"   - Salles: {total_salles}")

    except Exception as e:
        print(f"❌ Erreur lors de l'importation: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Début de l'importation des données de référence...\n")
    import_data()
