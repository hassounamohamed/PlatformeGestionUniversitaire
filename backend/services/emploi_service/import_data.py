"""
Script pour importer les données de référence (matières, enseignants, salles, groupes)
dans la base de données emploi_service.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

# Database configuration
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/gestion_universitaire"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define reference tables
class Matiere(Base):
    __tablename__ = "matieres"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, nullable=False, index=True)
    code = Column(String, unique=True, nullable=True)

class Enseignant(Base):
    __tablename__ = "enseignants"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True)

class Salle(Base):
    __tablename__ = "salles"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, nullable=False, index=True)
    capacite = Column(Integer, default=30)
    type_salle = Column(String, default="Labo")

class Groupe(Base):
    __tablename__ = "groupes"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, nullable=False, index=True)
    niveau = Column(String, nullable=True)
    specialite = Column(String, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Data to import
DATA = {
    "matieres": [
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
        "Atelier Base de Données"
    ],
    "enseignants": [
        "Sarra Jemli",
        "Wafa Zarroug",
        "Houda Najjari",
        "Yousra Ghaouar",
        "Daoud Salah",
        "Ibrahim Chrait",
        "Fadwa Touati",
        "Taher Ben Youssef",
        "Taheya Baccari",
        "Taha Sfaya",
        "Mohamed Mbarki",
        "Soufiene B.M",
        "Ebtihal Hadfi",
        "Haifa Touati",
        "Bilel Chraigui",
        "Dzirya Arfaoui",
        "Haithem Hafsi",
        "Haifa Dguechi",
        "Hamed Benneji",
        "Mariem Jeridi",
        "Ibtikhar Chetoui",
        "Takwa Omrani",
        "Ebtihal Hedfi"
    ],
    "salles": [
        "LI 07",
        "LG 01",
        "SI 03",
        "SI 04",
        "LG 04",
        "SI 09",
        "LI 03",
        "LI 06",
        "SI 01",
        "AMPHI",
        "LI 05"
    ],
    "groupes": [
        "TI11", "TI12", "TI13", "TI14", "TI15", "TI16", "TI17", "TI18",
        "DSI21", "DSI22", "DSI23", "RSI21",
        "DSI31", "DSI32", "RSI31"
    ]
}

def import_data():
    """Import all reference data into database, avoiding duplicates."""
    db = SessionLocal()
    
    try:
        # Import Matières
        print("\n📚 Importation des matières...")
        matiere_count = 0
        for nom in sorted(set(DATA["matieres"])):  # Remove duplicates
            try:
                existing = db.query(Matiere).filter(Matiere.nom == nom).first()
                if not existing:
                    matiere = Matiere(nom=nom)
                    db.add(matiere)
                    db.commit()
                    matiere_count += 1
                    print(f"  ✓ {nom}")
                else:
                    print(f"  ⊙ {nom} (existe déjà)")
            except IntegrityError:
                db.rollback()
                print(f"  ✗ {nom} (erreur)")
        
        print(f"\n✅ {matiere_count} matières importées")
        
        # Import Enseignants
        print("\n👨‍🏫 Importation des enseignants...")
        enseignant_count = 0
        for nom in sorted(set(DATA["enseignants"])):  # Remove duplicates
            try:
                existing = db.query(Enseignant).filter(Enseignant.nom == nom).first()
                if not existing:
                    enseignant = Enseignant(nom=nom)
                    db.add(enseignant)
                    db.commit()
                    enseignant_count += 1
                    print(f"  ✓ {nom}")
                else:
                    print(f"  ⊙ {nom} (existe déjà)")
            except IntegrityError:
                db.rollback()
                print(f"  ✗ {nom} (erreur)")
        
        print(f"\n✅ {enseignant_count} enseignants importés")
        
        # Import Salles
        print("\n🏫 Importation des salles...")
        salle_count = 0
        for numero in sorted(set(DATA["salles"])):  # Remove duplicates
            try:
                existing = db.query(Salle).filter(Salle.numero == numero).first()
                if not existing:
                    salle = Salle(numero=numero)
                    db.add(salle)
                    db.commit()
                    salle_count += 1
                    print(f"  ✓ {numero}")
                else:
                    print(f"  ⊙ {numero} (existe déjà)")
            except IntegrityError:
                db.rollback()
                print(f"  ✗ {numero} (erreur)")
        
        print(f"\n✅ {salle_count} salles importées")
        
        # Import Groupes
        print("\n👥 Importation des groupes...")
        groupe_count = 0
        for nom in sorted(set(DATA["groupes"])):  # Remove duplicates
            try:
                existing = db.query(Groupe).filter(Groupe.nom == nom).first()
                if not existing:
                    # Extract niveau and specialite
                    niveau = nom[:3] if len(nom) >= 3 else nom
                    if "TI" in nom:
                        specialite = "Technologies de l'Informatique"
                    elif "DSI" in nom:
                        specialite = "Développement de Systèmes d'Information"
                    elif "RSI" in nom:
                        specialite = "Réseaux et Systèmes Informatiques"
                    else:
                        specialite = "Informatique"
                    
                    groupe = Groupe(nom=nom, niveau=niveau, specialite=specialite)
                    db.add(groupe)
                    db.commit()
                    groupe_count += 1
                    print(f"  ✓ {nom} ({specialite})")
                else:
                    print(f"  ⊙ {nom} (existe déjà)")
            except IntegrityError:
                db.rollback()
                print(f"  ✗ {nom} (erreur)")
        
        print(f"\n✅ {groupe_count} groupes importés")
        
        # Summary
        print("\n" + "="*60)
        print("📊 RÉSUMÉ DE L'IMPORTATION")
        print("="*60)
        print(f"Matières:    {matiere_count} nouvelles / {len(set(DATA['matieres']))} total")
        print(f"Enseignants: {enseignant_count} nouveaux / {len(set(DATA['enseignants']))} total")
        print(f"Salles:      {salle_count} nouvelles / {len(set(DATA['salles']))} total")
        print(f"Groupes:     {groupe_count} nouveaux / {len(set(DATA['groupes']))} total")
        print("="*60)
        
        # Display unique counts
        total_matieres = db.query(Matiere).count()
        total_enseignants = db.query(Enseignant).count()
        total_salles = db.query(Salle).count()
        total_groupes = db.query(Groupe).count()
        
        print(f"\n🗄️  Total dans la base de données:")
        print(f"   Matières:    {total_matieres}")
        print(f"   Enseignants: {total_enseignants}")
        print(f"   Salles:      {total_salles}")
        print(f"   Groupes:     {total_groupes}")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("="*60)
    print("📥 IMPORTATION DES DONNÉES DE RÉFÉRENCE")
    print("="*60)
    import_data()
    print("\n✅ Importation terminée!\n")
