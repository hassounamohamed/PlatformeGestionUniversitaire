-- Création des tables Niveau et Groupe dans referentiel_db

-- 1. Créer la table niveaux
CREATE TABLE IF NOT EXISTS niveaux (
    id SERIAL PRIMARY KEY,
    nom VARCHAR NOT NULL UNIQUE,
    specialite_id INTEGER REFERENCES matieres(id) ON DELETE SET NULL
);

-- 2. Créer la table groupes
CREATE TABLE IF NOT EXISTS groupes (
    id SERIAL PRIMARY KEY,
    nom VARCHAR NOT NULL UNIQUE,
    niveau_id INTEGER REFERENCES niveaux(id) ON DELETE SET NULL
);

-- 3. Mettre à jour la table etudiants pour ajouter les contraintes de clé étrangère
ALTER TABLE etudiants 
    DROP CONSTRAINT IF EXISTS etudiants_groupe_id_fkey,
    DROP CONSTRAINT IF EXISTS etudiants_specialite_id_fkey;

ALTER TABLE etudiants 
    ADD CONSTRAINT etudiants_groupe_id_fkey 
    FOREIGN KEY (groupe_id) REFERENCES groupes(id) ON DELETE SET NULL;

ALTER TABLE etudiants 
    ADD CONSTRAINT etudiants_specialite_id_fkey 
    FOREIGN KEY (specialite_id) REFERENCES matieres(id) ON DELETE SET NULL;

-- 4. Mettre à jour la table matieres pour ajouter credits et niveau_id
ALTER TABLE matieres 
    ADD COLUMN IF NOT EXISTS credits INTEGER,
    ADD COLUMN IF NOT EXISTS niveau_id INTEGER REFERENCES niveaux(id) ON DELETE SET NULL;

-- 5. Insérer des niveaux pour le département informatique
INSERT INTO niveaux (nom) VALUES 
    ('1ère année TI'),
    ('2ème année DSI'),
    ('2ème année RSI'),
    ('3ème année DSI'),
    ('3ème année RSI')
ON CONFLICT (nom) DO NOTHING;

-- 6. Insérer les groupes du département informatique
INSERT INTO groupes (nom, niveau_id) VALUES 
    ('TI11', (SELECT id FROM niveaux WHERE nom = '1ère année TI')),
    ('TI12', (SELECT id FROM niveaux WHERE nom = '1ère année TI')),
    ('TI13', (SELECT id FROM niveaux WHERE nom = '1ère année TI')),
    ('TI14', (SELECT id FROM niveaux WHERE nom = '1ère année TI')),
    ('TI15', (SELECT id FROM niveaux WHERE nom = '1ère année TI')),
    ('TI16', (SELECT id FROM niveaux WHERE nom = '1ère année TI')),
    ('TI17', (SELECT id FROM niveaux WHERE nom = '1ère année TI')),
    ('TI18', (SELECT id FROM niveaux WHERE nom = '1ère année TI')),
    ('DSI21', (SELECT id FROM niveaux WHERE nom = '2ème année DSI')),
    ('DSI22', (SELECT id FROM niveaux WHERE nom = '2ème année DSI')),
    ('DSI23', (SELECT id FROM niveaux WHERE nom = '2ème année DSI')),
    ('RSI21', (SELECT id FROM niveaux WHERE nom = '2ème année RSI')),
    ('DSI31', (SELECT id FROM niveaux WHERE nom = '3ème année DSI')),
    ('DSI32', (SELECT id FROM niveaux WHERE nom = '3ème année DSI')),
    ('RSI31', (SELECT id FROM niveaux WHERE nom = '3ème année RSI'))
ON CONFLICT (nom) DO NOTHING;

-- Afficher le résumé
SELECT 'Niveaux' as table_name, COUNT(*) as total FROM niveaux
UNION ALL
SELECT 'Groupes', COUNT(*) FROM groupes;
