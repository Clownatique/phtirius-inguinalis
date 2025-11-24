--- SCRIPT SQL CREATION DES TABLES ---

DROP SCHEMA IF EXISTS morpion CASCADE;
CREATE SCHEMA morpion;
SET SEARCH_PATH TO morpion;

CREATE EXTENSION "uuid-ossp";

CREATE TABLE Equipe(
    PRIMARY KEY (nomE),
    nomE VARCHAR(16) NOT NULL,
    couleurE VARCHAR(6) UNIQUE NOT NULL,
    date_creation DATE
);

CREATE TABLE Morpion(
    idM SERIAL PRIMARY KEY,
    nomM VARCHAR(30),
    image VARCHAR(90),
    PV  INTEGER,
    ATK INTEGER,
    MANA INTEGER,
    REU INTEGER
);

CREATE TABLE Posseder(
    PRIMARY KEY (idM, nomE),
    FOREIGN KEY (idM) REFERENCES Morpion(idM),
    FOREIGN KEY (nomE) REFERENCES Equipe(nomE),
    idM INTEGER NOT NULL, -- clé étrangère
    nomE VARCHAR(16) NOT NULL-- clé étrangère
);

CREATE TABLE Partie (
    idp UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nomE1 VARCHAR(16) NOT NULL,
    nomE2 VARCHAR(16) NOT NULL, -- clé étrangère
    date_debut DATE,
    date_fin DATE,
    max_tours INTEGER,
    taille_grille INTEGER,
    est_speciale BOOL,
    FOREIGN KEY (nome1) REFERENCES Equipe(nomE),
    FOREIGN KEY (nome2) REFERENCES Equipe(nomE)
);

CREATE TABLE Journal(
    numA  INTEGER UNIQUE NOT NULL,
    date_action DATE,
    texte_action VARCHAR(80),
    date_debut DATE,
    idp UUID,
    PRIMARY KEY (numA,idp),
    FOREIGN KEY (idP) REFERENCES Partie(idp)
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

INSERT INTO Partie (nomE1,nomE2,date_debut,max_tours,taille_grille) VALUES
('abricotiers','pommiers',NOW(),64,3);
