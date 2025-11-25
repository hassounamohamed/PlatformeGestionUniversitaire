"""
Script pour insérer directement les données dans referentiel_db
"""
import psycopg2
from psycopg2.extras import execute_values

# Connexion à la base de données
conn = psycopg2.connect(
    host="localhost",
    database="referentiel_db",
    user="postgres",
    password="root"
)
conn.set_client_encoding('UTF8')
cur = conn.cursor()

try:
    print("🚀 Insertion des données de référence...\n")
    
    # 1. Créer le département Informatique s'il n'existe pas
    cur.execute("""
        INSERT INTO departements (nom, code) 
        VALUES ('Informatique', 'INFO')
        ON CONFLICT (code) DO NOTHING
        RETURNING id
    """)
    
    result = cur.fetchone()
    if result:
        dept_id = result[0]
        print(f"✅ Département Informatique créé (ID: {dept_id})")
    else:
        cur.execute("SELECT id FROM departements WHERE code = 'INFO'")
        dept_id = cur.fetchone()[0]
        print(f"✓ Département Informatique existe déjà (ID: {dept_id})")
    
    # 2. Insérer les enseignants
    enseignants_data = [
        ('Sarra', 'Jemli', 'sarra.jemli@iset.tn', dept_id),
        ('Wafa', 'Zarroug', 'wafa.zarroug@iset.tn', dept_id),
        ('Houda', 'Najjari', 'houda.najjari@iset.tn', dept_id),
        ('Yousra', 'Ghaouar', 'yousra.ghaouar@iset.tn', dept_id),
        ('Daoud', 'Salah', 'daoud.salah@iset.tn', dept_id),
        ('Ibrahim', 'Chrait', 'ibrahim.chrait@iset.tn', dept_id),
        ('Fadwa', 'Touati', 'fadwa.touati@iset.tn', dept_id),
        ('Taher', 'Ben Youssef', 'taher.benyoussef@iset.tn', dept_id),
        ('Taheya', 'Baccari', 'taheya.baccari@iset.tn', dept_id),
        ('Taha', 'Sfaya', 'taha.sfaya@iset.tn', dept_id),
        ('Mohamed', 'Mbarki', 'mohamed.mbarki@iset.tn', dept_id),
        ('Soufiene', 'B.M', 'soufiene.bm@iset.tn', dept_id),
        ('Ebtihal', 'Hadfi', 'ebtihal.hadfi@iset.tn', dept_id),
        ('Haifa', 'Touati', 'haifa.touati@iset.tn', dept_id),
        ('Bilel', 'Chraigui', 'bilel.chraigui@iset.tn', dept_id),
        ('Dzirya', 'Arfaoui', 'dzirya.arfaoui@iset.tn', dept_id),
        ('Haithem', 'Hafsi', 'haithem.hafsi@iset.tn', dept_id),
        ('Haifa', 'Dguechi', 'haifa.dguechi@iset.tn', dept_id),
        ('Hamed', 'Benneji', 'hamed.benneji@iset.tn', dept_id),
        ('Mariem', 'Jeridi', 'mariem.jeridi@iset.tn', dept_id),
        ('Ibtikhar', 'Chetoui', 'ibtikhar.chetoui@iset.tn', dept_id),
        ('Takwa', 'Omrani', 'takwa.omrani@iset.tn', dept_id),
        ('Ebtihal', 'Hedfi', 'ebtihal.hedfi@iset.tn', dept_id),
        ('Wahbi', 'Rajhi', 'wahbi.rajhi@iset.tn', dept_id),
        ('Rana', 'Rhili', 'rana.rhili@iset.tn', dept_id),
    ]
    
    cur.execute("SELECT COUNT(*) FROM enseignants")
    before_count = cur.fetchone()[0]
    
    for prenom, nom, email, did in enseignants_data:
        cur.execute("""
            INSERT INTO enseignants (prenom, nom, email, departement_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
        """, (prenom, nom, email, did))
    
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM enseignants")
    after_count = cur.fetchone()[0]
    created = after_count - before_count
    print(f"✅ {created} enseignants créés ({after_count} total)")
    
    # 3. Insérer les matières
    matieres_data = [
        ('Développement Web et Multimédia I', 'DEV_WEB_MM1', 3, dept_id),
        ('Atelier Développement Web et Multimédia I', 'AT_DEV_WEB1', 2, dept_id),
        ('Atelier Programmation', 'AT_PROG', 2, dept_id),
        ('Atelier Mathématiques', 'AT_MATH', 2, dept_id),
        ('Atelier Systèmes Logiques', 'AT_SYS_LOG', 2, dept_id),
        ('Business Culture', 'BUS_CULT', 2, dept_id),
        ('Architecture des Ordinateurs', 'ARCHI_ORD', 3, dept_id),
        ('English for Computing 1', 'ENG_COMP1', 2, dept_id),
        ('Algorithmique & Programmation 1', 'ALGO_PROG1', 3, dept_id),
        ('Bureautique', 'BUREAU', 2, dept_id),
        ('Mathématique Appliquée', 'MATH_APP', 3, dept_id),
        ('Technique d\'expression 1', 'TECH_EXP1', 2, dept_id),
        ('2CN', '2CN', 2, dept_id),
        ('Administration Systèmes', 'ADM_SYS', 3, dept_id),
        ('LPIC1', 'LPIC1', 3, dept_id),
        ('Communication en entreprise', 'COM_ENT', 2, dept_id),
        ('Bases de Données', 'BDD', 3, dept_id),
        ('Atelier Bases de Données', 'AT_BDD', 2, dept_id),
        ('Atelier Programmation Objet', 'AT_POO', 2, dept_id),
        ('Réseaux Locaux & TCP/IP', 'RES_TCPIP', 3, dept_id),
        ('Droit de l\'Informatique & Propriétés', 'DROIT_INFO', 2, dept_id),
        ('High Tech English', 'HT_ENG', 2, dept_id),
        ('Cybersecurity Essentials', 'CYBER_ESS', 3, dept_id),
        ('Programmation Objet', 'POO', 3, dept_id),
        ('Modélisation Objet (UML2)', 'UML2', 3, dept_id),
        ('Outils de Développement Collaboratif', 'OUT_DEV_COL', 2, dept_id),
        ('Programmation Python Avancée', 'PYTHON_ADV', 3, dept_id),
        ('Atelier Développement Web côté Serveur', 'AT_WEB_SRV', 2, dept_id),
        ('Atelier Framework côté Client', 'AT_FW_CLI', 2, dept_id),
        ('Systèmes Logiques', 'SYS_LOG', 3, dept_id),
        ('IT Essentials', 'IT_ESS', 2, dept_id),
    ]
    
    cur.execute("SELECT COUNT(*) FROM matieres")
    before_count = cur.fetchone()[0]
    
    for nom, code, credits, did in matieres_data:
        cur.execute("""
            INSERT INTO matieres (nom, code, credits, departement_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (code) DO NOTHING
        """, (nom, code, credits, did))
    
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM matieres")
    after_count = cur.fetchone()[0]
    created = after_count - before_count
    print(f"✅ {created} matières créées ({after_count} total)")
    
    # 4. Insérer les salles
    salles_data = [
        ('LI 03', 'Laboratoire Informatique', 30),
        ('LI 05', 'Laboratoire Informatique', 30),
        ('LI 06', 'Laboratoire Informatique', 30),
        ('LI 07', 'Laboratoire Informatique', 30),
        ('LG 01', 'Laboratoire Gestion', 30),
        ('LG 04', 'Laboratoire Gestion', 30),
        ('SI 01', 'Salle Informatique', 40),
        ('SI 02', 'Salle Informatique', 40),
        ('SI 03', 'Salle Informatique', 40),
        ('SI 04', 'Salle Informatique', 40),
        ('SI 09', 'Salle Informatique', 40),
        ('AMPHI', 'Amphithéâtre', 100),
    ]
    
    cur.execute("SELECT COUNT(*) FROM salles")
    before_count = cur.fetchone()[0]
    
    for numero, type_salle, capacite in salles_data:
        cur.execute("""
            INSERT INTO salles (numero, type, capacite)
            VALUES (%s, %s, %s)
            ON CONFLICT (numero) DO NOTHING
        """, (numero, type_salle, capacite))
    
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM salles")
    after_count = cur.fetchone()[0]
    created = after_count - before_count
    print(f"✅ {created} salles créées ({after_count} total)")
    
    print("\n🎉 Importation terminée avec succès!")
    print("\n📊 Résumé:")
    
    cur.execute("SELECT COUNT(*) FROM departements")
    print(f"   • Départements: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM enseignants")
    print(f"   • Enseignants: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM matieres")
    print(f"   • Matières: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM salles")
    print(f"   • Salles: {cur.fetchone()[0]}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    conn.rollback()
    raise
finally:
    cur.close()
    conn.close()
