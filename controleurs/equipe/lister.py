from model.equipe import liste_equipes

REQUEST_VARS['liste_equipe'] = liste_equipes(SESSION['CONNEXION'])

# peut être faire une page de recherche ?
