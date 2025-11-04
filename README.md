# Instructions pour un espace de travail

à faire avant de clone le repo (car il manque le serveur !)

```bash
curl https://perso.liris.cnrs.fr/fabien.duchateau/ens/BDW/tp/bdw-server.zip --output bdw.zip
mkdir nom_espace
python -m venv espace
source espace/bin/activate
cd websites
git clone git@github.com:Clownatique/phtirius-inguinalis.git
cd phtirius-inguinalis
```

à faire avant de coder: 

```bash
#on suppose donc être dans phtirius-inguinalis
git pull
```

après avoir codé:

```bash
git add .
git commit -m 'message' 
```
pour les messages:
nom de la sous/fonctionnalité codé, en précisant si il s'agit du modèle, de la vue ou du contrôlleur

# phtirius-inguinalis



## Fonctionnalité 1 : accueil et statistiques
Concevez la page d’accueil de votre site. Personnalisez-la comme vous le souhaitez (e.g., objectifs du site, tutoriel).

Nombre d’instances pour 3 tables de votre choix 
- [ ] Top-3 des équipes avec le plus de victoires 
- [ ] Partie la plus rapide et celle la plus longue 
- [ ] Nombre moyen de lignes de journalisation, pour chaque couple (mois, année).

le controleur accueil ne gère pour l'instant pas grand chose
il utilise un système de bloque pour scinder les statistiques en deux
## Fonctionnalité 2 : gestion des équipes
Cette seconde fonctionnalité consiste à créer et supprimer une équipe :
- [ ] Ajouter une dizaine de morpions directement dans votre BD (e.g., avec des requêtes SQL). Vous devez
obligatoirement utiliser les images fournies pour les morpions ;
- [ ] Développer une page qui permet de créer une nouvelle équipe, en sélectionnant des morpions parmi ceux
présents dans la BD ;
- [ ] Développer une page qui liste les équipes disponibles, et qui permet de supprimer une équipe.
## Fonctionnalité 3 : partie normale
Cette fonctionnalité permet à 2 personnes de jouer une partie normale (sans les règles avancées) :
- [ ] Développer une page pour choisir 2 équipes, une taille de grille et un nombre maximal de tours. Ces 2
derniers paramètres constituent la configuration de la partie ;
- [ ] Développer une page pour gérer un tour de jeu. Vous êtes libres concernant le style graphique de la grille.
La joueuse dont c’est le tour choisit un morpion de son équipe et une case libre où le placer ;
- [ ] Vérifier les conditions d’arrêt (victoire, grille pleine, nombre de tours atteint).
Les informations sur la partie seront progressivement stockées en base de données, en particulier dans le journal.
Réfléchissez aux structures de données (en prenant en compte la fonctionnalité 4). Pensez à gérer les erreurs
(messages pertinents).
## Fonctionnalité 4 : partie avancée
L’objectif est de créer une nouvelle page pour jouer
avec les règles avancées. Il est fortement conseillé
de conserver la fonctionnalité 3 et de créer de nou-
veaux fichiers. La page qui gère le tour permet en
plus de gérer les combats et les sorts.
Lors de la soutenance, il est fort probable que les
enseignant·e·s testent votre application en saisis-
sant des valeurs absurdes susceptibles de déclen-
cher des erreurs dans votre application. Alors es-
sayez de penser au pire ! Libres à vous d’ajouter
de nouvelles fonctionnalités (e.g., partie contre la
machine, nouveaux sorts).
Exemple de grille (ici victoire de la joueuse verte)
## Préparation des livrables
Deux livrables sont à rendre le jour de soutenance de votre projet, avant 23h59, sur Tomuss :
- [ ] Une archive de votre site web, en zip ou rar (colonne archive_projet), qui contient a-minima :
– le répertoire de votre site (code complet, commenté et indenté, respectant l’arborescence de la section
2 et incluant votre fichier de configuration config.toml) ;
– les fichiers de conception de la BD, i.e., le diagramme entité/association (format png ou pdf), le
schéma relationnel sous forme textuelle (format txt, pdf, html, ou markdown) et le script SQL
exécutable de création de votre base de données avec des instances en nombre suffisant (format txt
ou sql).
- [ ] Une affiche en pdf, de 1 page maximum (colonne affiche_projet). Ce document n’est pas évalué directe-
ment, mais offre à vos enseignant·e·s un aperçu de votre site (sans l’installer), notamment pour harmoniser
les notes après la soutenance. Sur cette affiche (au style graphique libre), vous mettrez :
– les noms et prénoms du binôme ;
– un résumé des fonctionnalités implémentées (e.g., sous forme de liste ou tableau) ;
– le diagramme entité/association ;
– des captures d’écran annotées de votre site.
