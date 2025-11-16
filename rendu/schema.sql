--- SCRIPT SQL CREATION DES TABLES ---

DROP SCHEMA IF EXISTS morpion CASCADE;
CREATE SCHEMA morpion;
SET SEARCH_PATH TO morpion;

CREATE TABLE Equipe(
    PRIMARY KEY (nomE, couleurE),
    nomE VARCHAR(16) NOT NULL,
    couleurE INTEGER NOT NULL,
    date_creation DATE,
);

CREATE TABLE Morpion(
    PRIMARY KEY (idM),
    idM INTEGER NOT NULL,
    nomM VARCHAR(30);
    image VARCHAR(90),
    PV  INTEGER,
    ATK INTEGER,
    MANA INTEGER,
    REU INTEGER,
);

CREATE TABLE Posseder(
    PRIMARY KEY (idM, nomE, couleurE),
    FOREIGN KEY (idM) REFERENCES Morpion(idM),
    FOREIGN KEY (nomE, couleurE) REFERENCES Equipe(nomE, couleurE),
    idM INTEGER NOT NULL, -- clé étrangère
    nomE VARCHAR(16) NOT NULL, -- clé étrangère
    couleurE INTEGER NOT NULL,
    PV  INTEGER,
    ATK INTEGER,
    MANA INTEGER,
    REU INTEGER,
);

CREATE TABLE Partie (
    PRIMARY KEY (idP),
    idP INTEGER NOT NULL,
    date_debut DATE,
    date_fin DATE,
    max_tours INTEGER,
    taille_grille INTEGER,
);

CREATE TABLE Journal(
    PRIMARY KEY (numA,idP),
    FOREIGN KEY (idP) REFERENCES Partie(idP),
    numA INTEGER NOT NULL,
    idP INTEGER NOT NULL,
    date_action DATE,
    texte_action VARCHAR(80),
);

CREATE TABLE Jouer(
    PRIMARY KEY (idP, nomE, couleurE),
    FOREIGN KEY(idP) REFERENCES Partie(idP),
    FOREIGN KEY(nomE, couleurE) REFERENCES Equipe(nomE, couleurE),
    idP INTEGER NOT NULL,
    nomE VARCHAR(16) NOT NULL,
    couleurE INTEGER NOT NULL,
    couleurE1 INTEGER, -- deux clés étrangères*
    nomE1 VARCHAR(16), 
    couleurE2 INTEGER,
    nomE2 VARCHAR(16),
);


--- INSERTION FICTIVE DE DONNEES DANS LES TABLES

-- EQUIPES
INSERT INTO Equipe VALUES
('Tigers', 1, '2024-12-01'),
('Dragons', 2, '2025-01-12');

-- MORPIONS
INSERT INTO Morpion VALUES
(1, 'FeuFollet', 'feu.png', 5, 4, 3, 3),
(2, 'Tanky', 'tank.png', 8, 2, 2, 3),
(3, 'Mageoux', 'mage.png', 4, 3, 6, 2);

-- POSSEDER
INSERT INTO Posseder VALUES
(1, 'Tigers', 1, 5,4,3,3),
(2, 'Tigers', 1, 8,2,2,3),
(3, 'Dragons', 2, 4,3,6,2);

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
