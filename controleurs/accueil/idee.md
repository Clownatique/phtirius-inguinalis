# nombre d'équipes enregistrés
# nombre de parties
# nombre de morpion possible d'être joués
#
# top 3 des équipes avec le plus de victoires
#
# partie la plus rapide
#
# partie la plus longue
#
# nombre ligne de journal par couples (années, mois)
#
#
SELECT COUNT(*) FROM Partie;
SELECT COUNT(*) FROM Equipe;
SELECT COUNT(*) FROM Morpion;
# avec les moyennes suivantes:
#
SELECT AVG(ATK),AVG(MANA),AVG(PV),AVG(RÉU) FROM Morpion;

SELECT * FROM Equipe

#SELECT MAX(numA), COUNT(numA) FROM JOURNAL j JOIN Partie p USING(j.idp) WHERE p.date_fin IS NOT NULL;
#renvoie le numéro des coups qui font gagné
#
select count(texte_action),texte_action from journal where numa = 1 group by texte_action;

select max(date_debut-date_fin), min(date_debut-date_fin) from partie
select min(date_debut-date_fin)

idée : organiser le code de tel sorte à avoir des couples de requête + description + clé dans le dictionnaire
pour n'avoir qu'à éxecuter qu'une fonction ? (genre on boucle sur ce qu'il y a à faire)
