from app.core.database import SessionLocal, engine, Base
from app.models.departement import Departement
from app.models.groupe import Groupe
from app.models.enseignant import Enseignant
from app.models.etudiant import Etudiant

def seed():
    db = SessionLocal()
    try:
        # ensure tables exist
        Base.metadata.create_all(bind=engine)

        # create departement 'Informatique' if missing
        dept = db.query(Departement).filter(Departement.nom == 'Informatique').first()
        if not dept:
            dept = Departement(nom='Informatique')
            db.add(dept)
            db.commit()
            db.refresh(dept)

        # create some groupes
        group_names = ['TI11','TI12','TI13','DSI21','DSI22','RSI31']
        groupes = []
        for g in group_names:
            obj = db.query(Groupe).filter(Groupe.nom == g).first()
            if not obj:
                obj = Groupe(nom=g, departement_id=dept.id)
                db.add(obj)
                db.commit()
                db.refresh(obj)
            groupes.append(obj)

        # create enseignants
        enseigs = [
            ('Ghaouar','Yousra','yousra.ghaouar@example.com'),
            ('BM','Soufiene','soufiene.bm@example.com'),
            ('Jemli','Sarra','sarra.jemli@example.com')
        ]
        for nom, prenom, email in enseigs:
            e = db.query(Enseignant).filter(Enseignant.email == email).first()
            if not e:
                e = Enseignant(nom=nom, prenom=prenom, email=email, departement_id=dept.id)
                db.add(e)
                db.commit()

        # create a few etudiants
        students = [
            ('Ben','Ali','ben.ali@example.com','TI11'),
            ('Trabelsi','Salma','salma.trabelsi@example.com','TI12'),
            ('Masmoudi','Khaled','khaled.masmoudi@example.com','DSI21')
        ]
        for nom, prenom, email, groupe_nom in students:
            s = db.query(Etudiant).filter(Etudiant.email == email).first()
            grp = db.query(Groupe).filter(Groupe.nom == groupe_nom).first()
            if not s:
                s = Etudiant(nom=nom, prenom=prenom, email=email, groupe_id=grp.id if grp else None)
                db.add(s)
                db.commit()

        print('Seeding complete')
    finally:
        db.close()

if __name__ == '__main__':
    seed()
