import sys
from pathlib import Path

service_dir = Path(__file__).parent
sys.path.insert(0, str(service_dir))

try:
    print("Import database...")
    from app.core.database import Ses
    print("Import models...")
    from app.models.matiere import Matiere
    from app.models.enseignant import Enseignant
    from app.models.salle import Salle
    
    print("Création session...")
    db = SessionLocal()
    
    print("\n=== Test Matières ===")
    matieres = db.query(Matiere).limit(5).all()
    print(f"Nombre de matières: {len(matieres)}")
    for m in matieres[:3]:
        print(f"  - {m.nom} (ID: {m.id})")
    
    print("\n=== Test Enseignants ===")
    enseignants = db.query(Enseignant).limit(5).all()
    print(f"Nombre d'enseignants: {len(enseignants)}")
    for e in enseignants[:3]:
        print(f"  - {e.nom} {e.prenom} (ID: {e.id})")
    
    print("\n=== Test Salles ===")
    salles = db.query(Salle).limit(5).all()
    print(f"Nombre de salles: {len(salles)}")
    for s in salles[:3]:
        print(f"  - {s.code} - {s.type} (ID: {s.id})")
    
    db.close()
    print("\n✓ Tous les tests réussis!")
    
except Exception as e:
    print(f"\n✗ Erreur: {e}")
    import traceback
    traceback.print_exc()
