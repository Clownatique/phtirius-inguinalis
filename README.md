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
format des messages
nom de la sous/fonctionnalité codé, en précisant si il s'agit du modèle, de la vue ou du contrôlleur

# phtirius-inguinalis

## entité association

![Diagramme entité association de la base de donné](rendu/schema-ea.svg)

## schema relationnel

il est dispo ici [schema\_relationnel](rendu/schema_relationnel.md)

## fonctionnalités

### accueil et statistiques

-  Top-3 des équipes avec le plus de victoires
-  Partie la plus rapide et celle la plus longue
-  Nombre moyen de lignes de journalisation, pour chaque couple (mois,année).

- [ ] vue `templates/accueil/accueil.html + {{ block statistiques.html}}`
- [ ] modèle
- [ ] controlleur `controleurs/accueil/accueil.py`


le controleur accueil ne gère pour l'instant pas grand chose
il utilise un système de bloque pour scinder les statistiques en deux
### gestion des équipes

- [x] faire le script pour remplir la bdd avec les morpions (avec les images)

#### créer une nouvelle équipe

- [x] vue `templates/equipe/creation.html`
- [x] modèle
- [x] ~ controlleur `controleurs/equipe/creation.py`

#### lister les équipes

- [x] vue `templates/equipe/lister.html`
- [x] modèle
- [x] controlleur`controleurs/equipe/lister.py`

#### supprimer les équipes

- [x] vue `templates/equipe/lister.html`
- [x] modèle
- [x] controlleur`controleurs/equipe/lister.py`

### partie normale

#### pré partie

forms pour créer une instance partie

- [x] vue `templates/partie_simple/creation.html` (flora)
- [x] modèle (nestor)
- [x] controlleur `controleurs/partie/creation.py` (flora puis nestor)

#### pendant la partie

La joueuse dont c’est le tour choisit un morpion de son équipe et une case libre où le placer ;

- [x] vue `templates/partie_simple/jouer.html`
- [x] modèle
- [x] controlleur `controleurs/partie/jouer.py`

En somme, c une création d'action dans la base.
après avoir inséré l'action, vérifié si la partie est réussie. Si elle est
réussie, il suffit d'afficher la page de poste partie
donc c un form + une insertion + verification de si le coup n'est pas illégal

#### post partie

Je pensais à une bête variation de la page "pendant la partie"
(victoire, grille pleine, nombre de tours atteint).

- [ ] vue `templates/partie/resultat.html`
- [ ] modèle
- [ ] controleur `templates/partie_simple/resultat.py`

### partie avancée

Il faudrait réutiliser les mêmes pages pour éviter la redondance
j'ai oublié de rajouter l'action `poser` dans le schéma ci dessous

![schéma des actions possible pour un tour](schema_tour.jpg)

### Préparation des livrables

ce qui concerne le livrable se trouve dans [ce dossier](rendu/README.md)
