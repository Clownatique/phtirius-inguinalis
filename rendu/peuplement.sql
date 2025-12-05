DELETE FROM Equipe;
DELETE FROM Morpion;
DELETE FROM Posseder;
DELETE FROM Partie;
DELETE FROM Journal;
-- EQUIPES
INSERT INTO Equipe (nome,couleure,date_creation) VALUES
('Tigers', 'ececec', NOW()),
('Dragons', 'dadada', NOW()),
('abricotiers','eeceed', NOW()),
('pommiers', '8c8c8c', NOW());

-- MORPIONS
INSERT INTO Morpion (nomm, image,pv,atk,mana,reu) VALUES
('nom_morpion_1','t1.png', 5, 5, 3, 2),
('nom_morpion_2','t2.png', 4, 4, 5, 2),
('nom_morpion_3','t3.png', 6, 3, 4, 2),
('nom_morpion_4','t4.png', 3, 6, 4, 2),
('nom_morpion_5','t5.png', 2, 3, 5, 5),
('nom_morpion_6','t6.png', 7, 4, 2, 2),
('nom_morpion_7','t7.png', 3, 5, 5, 2),
('nom_morpion_8','t8.png', 4, 2, 6, 3),
('nom_morpion_9','t9.png', 2, 2, 5, 6),
('nom_morpion_10','t10.png', 5, 5, 4, 1),
('nom_morpion_11','t11.png', 6, 5, 1, 3),
('nom_morpion_12','t12.png', 3, 4, 5, 3),
('nom_morpion_13','t13.png', 3, 7, 3, 2),
('nom_morpion_14','t14.png', 8, 1, 5, 1),
('nom_morpion_15','t15.png', 7, 1, 6, 1),
('nom_morpion_16','t16.png', 5, 4, 5, 1);
-- POSSEDER
INSERT INTO Posseder (idm, nome) VALUES
(1, 'Tigers'),
(2, 'Tigers'),
(4, 'Dragons'),
(8,'abricotiers'),
(5,'abricotiers'),
(6,'abricotiers'),
(1,'pommiers'),
(2,'pommiers'),
(3,'pommiers'),
(4,'pommiers'),
(5,'pommiers');

INSERT INTO Partie (idp,nomE1,nomE2,date_debut,max_tours,taille_grille,est_speciale) VALUES
('711228c0-d551-40ee-9757-680703c82afa','abricotiers','pommiers',NOW(),64,3,False),
('903843bd-2f39-4a82-adb3-13bd99c1f932','Tigers','Dragons','2025-11-24T23:44:39.028332+01:00',15,9,False),
('c25aa76f-d6da-420c-80b2-7d775962bbbf','pommiers','Dragons',NOW(),2,3,True);

INSERT INTO Journal (numa,date_action,texte_action,idp) values
(1,'2025-11-24T23:46:39.028332+01:00','0,2','903843bd-2f39-4a82-adb3-13bd99c1f932'),
(2,'2025-11-24T23:51:39.028332+01:00','1,2','903843bd-2f39-4a82-adb3-13bd99c1f932');
--(3,'2025-11-24T23:52:39.028332+01:00','1,0','903843bd-2f39-4a82-adb3-13bd99c1f932')
