--- SCRIPT SQL CREATION DES TABLES ---

DROP SCHEMA IF EXISTS morpion CASCADE;
CREATE SCHEMA morpion;
SET SEARCH_PATH TO morpion;

CREATE EXTENSION "uuid-ossp";

CREATE TABLE Equipe(
    nomE VARCHAR(50) PRIMARY KEY,
    couleurE VARCHAR(7) UNIQUE NOT NULL,
    date_creation DATE --mettre à défaut l'instant présent ?
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
    date_debut DATE, -- mettre à defaut l'instant présent ? 
    date_fin DATE,
    
    max_tours INTEGER NOT NULL DEFAULT 50 CHECK (max_tours>0),
    taille_grille INTEGER NOT NULL DEFAULT 3 CHECK (taille_grille IN (3, 4)),
    tour_actuel INTEGER DEFAULT 1,
    est_terminee BOOLEAN DEFAULT FALSE,
    est_speciale BOOLEAN,
    FOREIGN KEY (nomE1) REFERENCES Equipe(nomE),
    FOREIGN KEY (nomE2) REFERENCES Equipe(nomE),
    FOREIGN KEY (nomE_gagnant) REFERENCES Equipe(nomE),
    
    CHECK (date_fin IS NULL OR date_fin >= date_debut),
    CHECK (tour_actuel <= max_tours)
);

CREATE TABLE Journal(
    numA INTEGER NOT NULL,
    date_action DATE, --pareil mettre par défaut l'instant présent ? mais je sais pas c'est quoi la syntaxe 
    type_action VARCHAR(20) CHECK (type_action IN ('placement', 'attaque', 'sort', 'fin_tour', 'victoire')),
    texte_action VARCHAR(100) NOT NULL,
    date_debut DATE, --c'est la date de quoi ça déjà ?
    --je pensais qu'on pouvait rajouter les id du morpion qui attaque et celui qui est victime un truc comme ça :
    --idM_acteur INTEGER,
    --idM_cible INTEGER,
    --FOREIGN KEY (idM_acteur) REFERENCES Morpion(idM),
    --FOREIGN KEY (idM_cible) REFERENCES Morpion(idM),
    idp UUID NOT NULL,
    PRIMARY KEY (numA,idp),
    FOREIGN KEY (idP) REFERENCES Partie(idp) ON DELETE CASCADE
);

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
    FOREIGN KEY (nomE) REFERENCES Equipe(idE),

    UNIQUE (idP, position_x, position_y),
    CHECK ((position_x IS NULL AND position_y IS NULL) OR (position_x IS NOT NULL AND position_y IS NOT NULL))
);
    





--- INSERTION FICTIVE DE DONNEES DANS LES TABLES

-- EQUIPES
INSERT INTO Equipe (nome,couleure,date_creation) VALUES
('Tigers', 'ececec', '2024-12-01'),
('Dragons', 'dadada', '2025-01-12');


INSERT INTO EQUIPE (nome, couleure, date_creation) VALUES
('abricotiers','eeceed', NOW()),
('pommiers', '8c8c8c', NOW());

-- MORPIONS
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t1.png', 5, 5, 3, 2);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t2.png', 4, 4, 5, 2);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t3.png', 6, 3, 4, 2);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t4.png', 3, 6, 4, 2);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t5.png', 2, 3, 5, 5);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t6.png', 7, 4, 2, 2);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t7.png', 3, 5, 5, 2);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t8.png', 4, 2, 6, 3);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t9.png', 2, 2, 5, 6);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t10.png', 5, 5, 5, 0);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t11.png', 6, 6, 0, 3);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t12.png', 0, 7, 5, 3);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t13.png', 3, 7, 5, 0);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t14.png', 8, 2, 5, 0);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t15.png', 7, 0, 8, 0);
INSERT INTO morpion (image, PV, ATK, MANA, REU) VALUES ('t16.png', 5, 5, 5, 0);
-- POSSEDER
INSERT INTO Posseder (idm, nome) VALUES
(1, 'Tigers'),
(2, 'Tigers'),
(4, 'Dragons'),
(8,'abricotiers'),
(5,'abricotiers'),
(6,'abricotiers');

INSERT INTO Partie (idp,nomE1,nomE2,date_debut,max_tours,taille_grille,est_speciale) VALUES
('711228c0-d551-40ee-9757-680703c82afa','abricotiers','pommiers',NOW(),64,3,False),
('903843bd-2f39-4a82-adb3-13bd99c1f932','Tigers','Dragons','2025-11-24T23:44:39.028332+01:00',15,9,False),
('c25aa76f-d6da-420c-80b2-7d775962bbbf','pommiers','Dragons',NOW(),2,3,True);

INSERT INTO Journal (numa,date_action,texte_action,idp) values
(1,'2025-11-24T23:46:39.028332+01:00','0,2','903843bd-2f39-4a82-adb3-13bd99c1f932'),
(2,'2025-11-24T23:51:39.028332+01:00','1,2','903843bd-2f39-4a82-adb3-13bd99c1f932');
--(3,'2025-11-24T23:52:39.028332+01:00','1,0','903843bd-2f39-4a82-adb3-13bd99c1f932');
