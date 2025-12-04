--- SCRIPT SQL CREATION DES TABLES ---

DROP SCHEMA IF EXISTS morpion CASCADE;
CREATE SCHEMA morpion;
SET SEARCH_PATH TO morpion;

CREATE EXTENSION "uuid-ossp";

CREATE TABLE Equipe(
    nomE VARCHAR(50) PRIMARY KEY,
    couleurE VARCHAR(7) UNIQUE NOT NULL,
    date_creation TIMESTAMP DEFAULT NOW() 
);

CREATE TABLE Morpion(
    idM SERIAL PRIMARY KEY,
    nomM VARCHAR(30) NOT NULL,
    image VARCHAR(90) NOT NULL,
    PV  INTEGER NOT NULL CHECK (PV>=1),
    ATK INTEGER NOT NULL CHECK (ATK >=1),
    MANA INTEGER NOT NULL CHECK (MANA>=1),
    REU INTEGER NOT NULL CHECK (REU>=1),
    CHECK (PV + ATK + MANA + REU = 15)
);

CREATE TABLE Posseder(
    idM INTEGER NOT NULL,
    nomE VARCHAR(16) NOT NULL,
    PRIMARY KEY (idM, nomE),
    FOREIGN KEY (idM) REFERENCES Morpion(idM) ON DELETE CASCADE, --pour supprimer les liens automatiquement si un morpion est supprimé
    FOREIGN KEY (nomE) REFERENCES Equipe(nomE) ON DELETE CASCADE
);

CREATE TABLE Partie (
    idp UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nomE1 VARCHAR(16) NOT NULL,
    nomE2 VARCHAR(16) NOT NULL,
    -- nomE_gagnant VARCHAR(16), on peut le retrouver (qui a fait la dernière action de la partie)
    date_debut TIMESTAMP DEFAULT NOW(), -- mettre à defaut l'instant présent ?
    date_fin TIMESTAMP DEFAULT NOW(),
    max_tours INTEGER NOT NULL DEFAULT 9,-- CHECK (max_tours>0),
    taille_grille INTEGER NOT NULL DEFAULT 3,-- CHECK (taille_grille IN (3, 16)),
    -- tour_actuel INTEGER DEFAULT 1, on peut aussi le retrouver (max(action) dans les actions liés à cette partie)
    -- est_terminee BOOLEAN DEFAULT FALSE, on peut aussi le retrouver (si date_fin != null)
    est_speciale BOOLEAN,
    FOREIGN KEY (nomE1) REFERENCES Equipe(nomE) ON DELETE CASCADE,
    FOREIGN KEY (nomE2) REFERENCES Equipe(nomE) ON DELETE CASCADE,
    -- FOREIGN KEY (nomE_gagnant) REFERENCES Equipe(nomE) ON DELETE CASCADE,

    CHECK (date_fin IS NULL OR date_fin >= date_debut)
);

CREATE TABLE Journal(
    numA INTEGER NOT NULL,
    type_action VARCHAR(20) CHECK (type_action IN ('placement', 'attaque', 'sort', 'fin_tour', 'victoire')),
    texte_action VARCHAR(100) NOT NULL,
    date_action TIMESTAMP DEFAULT NOW(), 
    -- c la date de l'action !

    --je pensais qu'on pouvait rajouter les id du morpion qui attaque et
    -- celui qui est victime un truc comme ça :
    --idM_acteur INTEGER,
    --idM_cible INTEGER,
    --FOREIGN KEY (idM_acteur) REFERENCES Morpion(idM),
    --FOREIGN KEY (idM_cible) REFERENCES Morpion(idM),
    --
    -- de la même manière que tomuss, il est intéressant de
    -- voir les actions comme des évenement  qui sont recompilés.
    -- tout les attributs rajoutés vont ainsi dans texte_action
    --
    -- jte rassure on peut tout à fait conserver toutes les infos:
    --
    -- il suffit d'établir une manière de coder les évenements sans ambiguités
    --
    -- je te propose qu'on le voit comme ça parce que j'ai l'impression que
    -- c'est à ça que ça sert
    idp UUID NOT NULL,
    PRIMARY KEY (numA,idp),
    FOREIGN KEY (idP) REFERENCES Partie(idp) ON DELETE CASCADE
);

"""
--!!faut qu'on conserve l'état des morpions pendant la partie!!
--je sais plus si on voulait mettre l'etat dans la table posseder ou pas, j'ai fais une table sinon mais jsp
CREATE TABLE Etat_Morpion(
    idEtat Serial PRIMARY KEY,
    idP UUID NOT NULL,
    idM INTEGER NOT NULL,
    nomE VARCHAR(16) NOT NULL,

    position_x INTEGER CHECK (position_x BETWEEN 0 AND 4),
    position_y INTEGER CHECK (position_y BETWEEN 0 AND 4),

    PV_actuel INTEGER NOT NULL CHECK (PV_actuel >=0),
    MANA_actuel INTEGER NOT NULL CHECK (MANA_actuel >=0),
    REU_actuel INTEGER NOT NULL CHECK (REU_actuel >=0),
    est_vivant BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (idP) REFERENCES Partie(idP) ON DELETE CASCADE,
    FOREIGN KEY (idM) REFERENCES Morpion(idM),
    FOREIGN KEY (nomE) REFERENCES Equipe(nomE),

    UNIQUE (idP, position_x, position_y),
    CHECK ((position_x IS NULL AND position_y IS NULL) OR (position_x IS NOT NULL AND position_y IS NOT NULL))
);

-- INSERTION FICTIVE DE DONNEES DANS LES TABLES
"""