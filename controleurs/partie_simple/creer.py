from model.equipe import liste_equipes

connexion = SESSION['CONNEXION']
REQUEST_VARS["equipes"] = liste_equipes(connexion)
