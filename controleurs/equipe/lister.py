from model.equipe import liste_equipes
from model.equipe import liste_morpion_une_equipe, supprimer_equipe

connexion = SESSION['CONNEXION']

REQUEST_VARS['equipes_seul'] = liste_equipes(connexion)
liste_equipe_morpion = []
for infoE in REQUEST_VARS['equipes_seul']:
    equipe_morpions = {}

    morpions = liste_morpion_une_equipe(connexion,infoE[0])
    equipe_morpions['info'] = infoE
    equipe_morpions['morpions'] = morpions
    liste_equipe_morpion.append(equipe_morpions)

print(liste_equipe_morpion)
REQUEST_VARS['liste_equipes'] = liste_equipe_morpion

if POST != {}:
    for nomequipe in POST.keys():
        supprimer_equipe(connexion, nom=nomequipe)
# peut être faire une page de recherche ?
