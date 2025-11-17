from model.equipe import liste_equipes
from model.equipe import liste_morpion_une_equipe

REQUEST_VARS['equipes_seul'] = liste_equipes(SESSION['CONNEXION'])
#ajout des trucs dans le truc tsais
liste_equipe_morpion = []
for infoE in REQUEST_VARS['equipes_seul']:
    equipe_morpions = {}

    morpions = liste_morpion_une_equipe(SESSION['CONNEXION'],infoE[0],infoE[1]) 
    equipe_morpions['info'] = infoE
    equipe_morpions['morpions'] = morpions 
    liste_equipe_morpion.append(equipe_morpions)

print(liste_equipe_morpion)
REQUEST_VARS['liste_equipes'] = liste_equipe_morpion

# peut être faire une page de recherche ?
