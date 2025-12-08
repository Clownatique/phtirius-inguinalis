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
    nomE_gagnant VARCHAR(16), 
    date_debut TIMESTAMP DEFAULT NOW(), 
    date_fin TIMESTAMP DEFAULT NOW(),
    max_tours INTEGER NOT NULL DEFAULT 9,-- CHECK (max_tours>0),
    taille_grille INTEGER NOT NULL DEFAULT 3,-- CHECK (taille_grille IN (3, 16)),
    -- tour_actuel INTEGER DEFAULT 1, on peut aussi le retrouver (max(action) dans les actions liés à cette partie)
    -- est_terminee BOOLEAN DEFAULT FALSE, on peut aussi le retrouver (si date_fin != null)
    est_speciale BOOLEAN,
    FOREIGN KEY (nomE1) REFERENCES Equipe(nomE) ON DELETE CASCADE,
    FOREIGN KEY (nomE2) REFERENCES Equipe(nomE) ON DELETE CASCADE,
    FOREIGN KEY (nomE_gagnant) REFERENCES Equipe(nomE) ON DELETE CASCADE,

    CHECK (date_fin IS NULL OR date_fin >= date_debut)
);

CREATE TABLE Journal(
    numA INTEGER NOT NULL,
    type_action VARCHAR(20) CHECK (type_action IN ('placement', 'attaque', 'sort', 'fin_tour', 'victoire')),
    texte_action VARCHAR(100) NOT NULL,
    date_action TIMESTAMP DEFAULT NOW(),
    -- de la même manière que tomuss, il est intéressant de
    -- voir les actions comme des évenement  qui sont recompilés.
    -- tout les attributs rajoutés vont ainsi dans texte_action
    --
    -- on peut tout à fait conserver toutes les infos:
    idp UUID NOT NULL,
    PRIMARY KEY (numA,idp),
    FOREIGN KEY (idP) REFERENCES Partie(idp) ON DELETE CASCADE
);