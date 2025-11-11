DROP SCHEMA IF EXISTS morpion CASCADE;
CREATE SCHEMA morpion;
SET SEARCH_PATH TO morpion;

CREATE TABLE partie (
    PRIMARY KEY (idP),
    idP INTEGER NOT NULL,
    date_debut date,
    date_fin date,
    max_tours INTEGER,
    taille_grille INTEGER,
);

CREATE TABLE journal(
  PRIMARY KEY (numA,idP),
  numA INTEGER NOT NULL,
  idP INTEGER NOT NULL,
  date_action DATE,
  texte_action VARCHAR(80),
);

ALTER TABLE partie ADD FOREIGN KEY (idP) REFERENCES partie (idP);

CREATE TABLE jouer(
  PRIMARY KEY (idP),
  couleurE1 INTEGER, -- deux clés étrangères
  nomE1 VARCHAR(), 
  couleurE2 INTEGER,
  nomE2 VARCHAR(),
);


ALTER TABLE jouer ADD FOREIGN KEY (couleurE1) REFERENCES equipe (couleurE);
ALTER TABLE jouer ADD FOREIGN KEY (nomE1) REFERENCES equipe (nomE);
ALTER TABLE jouer ADD FOREIGN KEY (couleurE2) REFERENCES equipe (couleurE);
ALTER TABLE jouer ADD FOREIGN KEY (nomE2) REFERENCES equipe (nomE);

CREATE TABLE posseder(
  PRIMARY KEY (idM, nomE, couleurE),
  idM INTEGER, -- clé étrangère
  nomE VARCHAR(16), -- clé étrangère
  couleurE INTEGER,
  PV  INTEGER,
  ATK INTEGER,
  MANA INTEGER,
  REU INTEGER,
);

ALTER TABLE posseder ADD FOREIGN KEY (idM) REFERENCES morpion (idM);
ALTER TABLE posseder ADD FOREIGN KEY (nomE) REFERENCES equipe (nomE);
ALTER TABLE posseder ADD FOREIGN KEY (couleurE) REFERENCES equipe (couleurE);

CREATE TABLE morpion(
  PRIMARY KEY (idM),
  idM INTEGER,
  image VARCHAR(90),
  PV  INTEGER,
  ATK INTEGER,
  MANA INTEGER,
  REU INTEGER,
);


CREATE TABLE equipe(
  PRIMARY KEY (nomE, couleurE),
  nomE VARCHAR(16),
  couleurE INTEGER,
  date_creation DATE,
);


INSERT INTO Miels VALUES(1, 'miel de Provence', 'lavande', 'IGP', 2005);
INSERT INTO Miels VALUES(2, 'miel de Provence', 'fleurs', 'IGP', 2005);
INSERT INTO Miels VALUES(3, 'miel des Vosges', 'sapin', 'AOC', 1996);
INSERT INTO Miels VALUES(4, 'miel d''Alsace', 'fleurs', 'IGP', 2005);
INSERT INTO Miels VALUES(5, 'miel d''Alsace', 'forêt', 'IGP', 2005);
INSERT INTO Miels VALUES(6, 'miel de Corse', 'maquis', 'AOC', NULL);
INSERT INTO Miels VALUES(7, 'mel de Galicia', 'fleurs', 'IGP', 2007);
INSERT INTO Abeilles VALUES(1, 'abeille noire', NULL, 1758);
INSERT INTO Abeilles VALUES(2, 'abeille jaune', 'Italie', 1806);
INSERT INTO Abeilles VALUES(3, 'abeille asiatique', 'Inde', 1793);
INSERT INTO Abeilles VALUES(4, 'abeille russe', 'Russie', NULL);
INSERT INTO Abeilles VALUES(5, 'abeille carniolienne', 'Slovénie', 1879);
INSERT INTO Abeilles VALUES(6, 'abeille ibérique', 'Portugal', 1999);
INSERT INTO Abeilles VALUES(7, 'abeille tueuse', 'Brésil', 1956);
INSERT INTO Produire VALUES(1, 1, 'été');
INSERT INTO Produire VALUES(1, 2, 'été');
INSERT INTO Produire VALUES(2, 3, 'été');
INSERT INTO Produire VALUES(3, 1, 'printemps');
INSERT INTO Produire VALUES(3, 3, 'printemps');
INSERT INTO Produire VALUES(3, 5, 'été');
INSERT INTO Produire VALUES(3, 7, 'été');
INSERT INTO Produire VALUES(4, 2, 'été');
INSERT INTO Produire VALUES(4, 3, 'été');
INSERT INTO Produire VALUES(4, 6, 'été');
INSERT INTO Produire VALUES(5, 1, 'été');
INSERT INTO Produire VALUES(5, 5, 'printemps');
INSERT INTO Produire VALUES(6, 5, 'été');
INSERT INTO Produire VALUES(6, 6, 'automne');
INSERT INTO Produire VALUES(6, 7, 'printemps');


