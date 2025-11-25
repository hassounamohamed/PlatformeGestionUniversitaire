-- Script SQL pour insérer les données de référence
-- Encodage: UTF-8

-- 1. Créer le département Informatique
INSERT INTO departements (nom, code) 
VALUES ('Informatique', 'INFO')
ON CONFLICT (code) DO NOTHING;

-- 2. Insérer les enseignants
INSERT INTO enseignants (prenom, nom, email, departement_id)
SELECT prenom, nom, email, (SELECT id FROM departements WHERE code = 'INFO')
FROM (VALUES
    ('Sarra', 'Jemli', 'sarra.jemli@iset.tn'),
    ('Wafa', 'Zarroug', 'wafa.zarroug@iset.tn'),
    ('Houda', 'Najjari', 'houda.najjari@iset.tn'),
    ('Yousra', 'Ghaouar', 'yousra.ghaouar@iset.tn'),
    ('Daoud', 'Salah', 'daoud.salah@iset.tn'),
    ('Ibrahim', 'Chrait', 'ibrahim.chrait@iset.tn'),
    ('Fadwa', 'Touati', 'fadwa.touati@iset.tn'),
    ('Taher', 'Ben Youssef', 'taher.benyoussef@iset.tn'),
    ('Taheya', 'Baccari', 'taheya.baccari@iset.tn'),
    ('Taha', 'Sfaya', 'taha.sfaya@iset.tn'),
    ('Mohamed', 'Mbarki', 'mohamed.mbarki@iset.tn'),
    ('Soufiene', 'B.M', 'soufiene.bm@iset.tn'),
    ('Ebtihal', 'Hadfi', 'ebtihal.hadfi@iset.tn'),
    ('Haifa', 'Touati', 'haifa.touati@iset.tn'),
    ('Bilel', 'Chraigui', 'bilel.chraigui@iset.tn'),
    ('Dzirya', 'Arfaoui', 'dzirya.arfaoui@iset.tn'),
    ('Haithem', 'Hafsi', 'haithem.hafsi@iset.tn'),
    ('Haifa', 'Dguechi', 'haifa.dguechi@iset.tn'),
    ('Hamed', 'Benneji', 'hamed.benneji@iset.tn'),
    ('Mariem', 'Jeridi', 'mariem.jeridi@iset.tn'),
    ('Ibtikhar', 'Chetoui', 'ibtikhar.chetoui@iset.tn'),
    ('Takwa', 'Omrani', 'takwa.omrani@iset.tn'),
    ('Ebtihal', 'Hedfi', 'ebtihal.hedfi@iset.tn'),
    ('Wahbi', 'Rajhi', 'wahbi.rajhi@iset.tn'),
    ('Rana', 'Rhili', 'rana.rhili@iset.tn')
) AS t(prenom, nom, email)
ON CONFLICT (email) DO NOTHING;

-- 3. Insérer les matières
INSERT INTO matieres (nom, code, credits, departement_id)
SELECT nom, code, credits, (SELECT id FROM departements WHERE code = 'INFO')
FROM (VALUES
    ('Développement Web et Multimédia I', 'DEV_WEB_MM1', 3),
    ('Atelier Développement Web et Multimédia I', 'AT_DEV_WEB1', 2),
    ('Atelier Programmation', 'AT_PROG', 2),
    ('Atelier Mathématiques', 'AT_MATH', 2),
    ('Atelier Systèmes Logiques', 'AT_SYS_LOG', 2),
    ('Business Culture', 'BUS_CULT', 2),
    ('Architecture des Ordinateurs', 'ARCHI_ORD', 3),
    ('English for Computing 1', 'ENG_COMP1', 2),
    ('Algorithmique & Programmation 1', 'ALGO_PROG1', 3),
    ('Bureautique', 'BUREAU', 2),
    ('Mathématique Appliquée', 'MATH_APP', 3),
    ('Technique d''expression 1', 'TECH_EXP1', 2),
    ('2CN', '2CN', 2),
    ('Administration Systèmes', 'ADM_SYS', 3),
    ('LPIC1', 'LPIC1', 3),
    ('Communication en entreprise', 'COM_ENT', 2),
    ('Bases de Données', 'BDD', 3),
    ('Atelier Bases de Données', 'AT_BDD', 2),
    ('Atelier Programmation Objet', 'AT_POO', 2),
    ('Réseaux Locaux & TCP/IP', 'RES_TCPIP', 3),
    ('Droit de l''Informatique & Propriétés', 'DROIT_INFO', 2),
    ('High Tech English', 'HT_ENG', 2),
    ('Cybersecurity Essentials', 'CYBER_ESS', 3),
    ('Programmation Objet', 'POO', 3),
    ('Modélisation Objet (UML2)', 'UML2', 3),
    ('Outils de Développement Collaboratif', 'OUT_DEV_COL', 2),
    ('Programmation Python Avancée', 'PYTHON_ADV', 3),
    ('Atelier Développement Web côté Serveur', 'AT_WEB_SRV', 2),
    ('Atelier Framework côté Client', 'AT_FW_CLI', 2),
    ('Systèmes Logiques', 'SYS_LOG', 3),
    ('IT Essentials', 'IT_ESS', 2)
) AS t(nom, code, credits)
ON CONFLICT (code) DO NOTHING;

-- 4. Insérer les salles
INSERT INTO salles (numero, type, capacite)
VALUES
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
    ('AMPHI', 'Amphithéâtre', 100)
ON CONFLICT (numero) DO NOTHING;

-- Afficher le résumé
SELECT 'Départements' as table_name, COUNT(*) as total FROM departements
UNION ALL
SELECT 'Enseignants', COUNT(*) FROM enseignants
UNION ALL
SELECT 'Matières', COUNT(*) FROM matieres
UNION ALL
SELECT 'Salles', COUNT(*) FROM salles;
