DROP SCHEMA IF EXISTS morpion CASCADE;
CREATE SCHEMA morpion;
SET SEARCH_PATH TO morpion;

CREATE TABLE partie (
    PRIMARY KEY (idP),
    idP INTEGER NOT NULL,
    date_debut date,
    date_fin date,
    max_tours INTEGER,
    taille_grille INTEGER);

CREATE TABLE journal(
  PRIMARY KEY (numA,idP),
  numA INTEGER NOT NULL,
  idP INTEGER NOT NULL,
  date_action DATE,
  texte_action VARCHAR(80)
);

ALTER TABLE journal ADD FOREIGN KEY (idP) REFERENCES partie (idP);

CREATE TABLE jouer(
  PRIMARY KEY (couleurE1,nomE1,couleurE2,nomE2,idP),
  idP INTEGER,
  couleurE1 INTEGER, -- deux clés étrangères
  nomE1 VARCHAR(16), 
  couleurE2 INTEGER,
  nomE2 VARCHAR(16)
);

CREATE TABLE equipe(
  PRIMARY KEY (nomE, couleurE),
  nomE VARCHAR(16),
  couleurE INTEGER,
  date_creation DATE
);


ALTER TABLE jouer ADD FOREIGN KEY (couleurE1) REFERENCES equipe (couleurE);
ALTER TABLE jouer ADD FOREIGN KEY (nomE1) REFERENCES equipe (nomE);
ALTER TABLE jouer ADD FOREIGN KEY (couleurE2) REFERENCES equipe (couleurE);
ALTER TABLE jouer ADD FOREIGN KEY (nomE2) REFERENCES equipe (nomE);
ALTER TABLE jouer ADD FOREIGN KEY (idP) REFERENCES partie (idP);

CREATE TABLE morpion(
  PRIMARY KEY (idM),
  idM INTEGER,
  image VARCHAR(90),
  PV  INTEGER,
  ATK INTEGER,
  MANA INTEGER,
  REU INTEGER
);
CREATE TABLE posseder(
  PRIMARY KEY (idM, nomE, couleurE),
  idM INTEGER, -- clé étrangère
  nomE VARCHAR(16), -- clé étrangère
  couleurE INTEGER,
  PV  INTEGER,
  ATK INTEGER,
  MANA INTEGER,
  REU INTEGER
);

ALTER TABLE posseder ADD FOREIGN KEY (idM) REFERENCES morpion (idM);
ALTER TABLE posseder ADD FOREIGN KEY (nomE) REFERENCES equipe (nomE);
ALTER TABLE posseder ADD FOREIGN KEY (couleurE) REFERENCES equipe (couleurE);
