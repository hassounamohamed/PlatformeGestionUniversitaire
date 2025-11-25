-- Migration pour ajouter les colonnes manquantes à la table emploi_temps

-- Vérifier et ajouter matiere_nom si elle n'existe pas
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='emploi_temps' AND column_name='matiere_nom') THEN
        ALTER TABLE emploi_temps ADD COLUMN matiere_nom VARCHAR;
        RAISE NOTICE 'Colonne matiere_nom ajoutée';
    ELSE
        RAISE NOTICE 'Colonne matiere_nom existe déjà';
    END IF;
END $$;

-- Vérifier et ajouter enseignant_nom si elle n'existe pas
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='emploi_temps' AND column_name='enseignant_nom') THEN
        ALTER TABLE emploi_temps ADD COLUMN enseignant_nom VARCHAR;
        RAISE NOTICE 'Colonne enseignant_nom ajoutée';
    ELSE
        RAISE NOTICE 'Colonne enseignant_nom existe déjà';
    END IF;
END $$;

-- Vérifier et ajouter groupe_nom si elle n'existe pas
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='emploi_temps' AND column_name='groupe_nom') THEN
        ALTER TABLE emploi_temps ADD COLUMN groupe_nom VARCHAR;
        RAISE NOTICE 'Colonne groupe_nom ajoutée';
    ELSE
        RAISE NOTICE 'Colonne groupe_nom existe déjà';
    END IF;
END $$;
