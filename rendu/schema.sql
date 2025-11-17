--- SCRIPT SQL CREATION DES TABLES ---

DROP SCHEMA IF EXISTS morpion CASCADE;
CREATE SCHEMA morpion;
SET SEARCH_PATH TO morpion;

CREATE TABLE Equipe(
    PRIMARY KEY (nomE, couleurE),
    nomE VARCHAR(16) NOT NULL,
    couleurE VARCHAR(6) NOT NULL,
    date_creation DATE
);

CREATE TABLE Morpion(
    PRIMARY KEY (idM),
    idM INTEGER NOT NULL,
    nomM VARCHAR(30),
    image VARCHAR(90),
    PV  INTEGER,
    ATK INTEGER,
    MANA INTEGER,
    REU INTEGER
);

CREATE TABLE Posseder(
    PRIMARY KEY (idM, nomE, couleurE),
    FOREIGN KEY (idM) REFERENCES Morpion(idM),
    FOREIGN KEY (nomE, couleurE) REFERENCES Equipe(nomE, couleurE),
    idM INTEGER NOT NULL, -- clé étrangère
    nomE VARCHAR(16) NOT NULL, -- clé étrangère
    couleurE VARCHAR(6) NOT NULL -- clé étrangère
    PV  INTEGER,
    ATK INTEGER,
    MANA INTEGER,
    REU INTEGER
);

CREATE TABLE Partie (
    PRIMARY KEY (idP),
    idP INTEGER NOT NULL,
    date_debut DATE,
    date_fin DATE,
    max_tours INTEGER,
    taille_grille INTEGER
);

CREATE TABLE Journal(
    PRIMARY KEY (numA,idP),
    FOREIGN KEY (idP) REFERENCES Partie(idP),
    numA INTEGER NOT NULL,
    idP INTEGER NOT NULL,
    date_action DATE,
    texte_action VARCHAR(80)
);

CREATE TABLE Jouer(
    PRIMARY KEY (idP, nomE, couleurE),
    FOREIGN KEY(idP) REFERENCES Partie(idP),
    FOREIGN KEY(nomE1, couleurE1) REFERENCES Equipe(nomE, couleurE),
    FOREIGN KEY(nomE2, couleurE2) REFERENCES Equipe(nomE, couleurE),
    idP INTEGER NOT NULL,
    couleurE1 VARCHAR(6), -- deux clés étrangères*
    nomE1 VARCHAR(16), 
    couleurE2 VARCHAR(6):
    nomE2 VARCHAR(16)
);


--- INSERTION FICTIVE DE DONNEES DANS LES TABLES

-- EQUIPES
INSERT INTO Equipe VALUES
('Tigers', 1, '2024-12-01'),
('Dragons', 2, '2025-01-12');

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
INSERT INTO Posseder VALUES
(1, 'Tigers', 1),
(2, 'Tigers', 1),
(3, 'Dragons', 2);

-- PARTIE
INSERT INTO Partie VALUES
(100, '2025-02-10', NULL, 20, 3);

-- JOUER (deux équipes dans la partie)
INSERT INTO Jouer VALUES
(100, 'Tigers', 1),
(100, 'Dragons', 2);

-- JOURNAL
INSERT INTO Journal VALUES
(1, 100, '2025-02-10', 'La partie commence !'),
(2, 100, '2025-02-10', 'Tigers place un morpion.');
