<<<<<<< HEAD
from model.partie import inserer_action, recuperer_partie
=======
from model.partie import (inserer_action, creer_partie, recompiler_partie, recuperer_partie, recompiler_partie_avancee, verifier_action)
from model.utils import select_query
>>>>>>> 30aed9cc0c0e22bc03c24277b306f288f1b36817

#pyright: reportUndefinedVariable=false

connexion = SESSION['CONNEXION']

def verification_gagnee(grille):
    taille = len(grille)

    for i in range(taille):
        if all(grille[i][j] == grille[i][0] and grille[i][j] != '' for j in range(taille)):
            return True
    for j in range(taille):
        if all(grille[i][j] == grille[0][j] and grille[i][j] != '' for i in range(taille)):
            return True
    if all(grille[i][i] == grille[0][0] and grille[i][i] != '' for i in range(taille)):
        return True
    if all(grille[i][taille - 1 - i] == grille[0][taille - 1] and grille[i][taille - 1 - i] != '' for i in range(taille)):
        return True

    return False

def verifier_action(action:str,jouer:str, partie:list):
    """
        PRENDS:- un tuple de 2 cases
               - une manière d'identifier un jour (string ?)
         RENDS:- un bool pour le contrôleur
               - un str pour la bd si c bon/un message d'erreur
    """
    pos_sou = action[0].split(',')
    print(partie)
    print(pos_sou)
    if partie[int(pos_sou[0])][int(pos_sou[1])] == 0:
        return True
    else:
        return False
        # REQUEST_VARS[""]= "j'en connais un qui bidouille et ça me plaît pas"
        # return False

if not('url_components' in REQUEST_VARS) or (REQUEST_VARS['url_components'][1] == ''):
    # on vérifie l'url
    REQUEST_VARS['erreur'] = "erreur"
else:
    idp = REQUEST_VARS['url_components'][1]
    partie = recuperer_partie(connexion,idp)
    REQUEST_VARS['partie'] = partie
    print(partie)
    REQUEST_VARS['grille'] = partie['grille']
    REQUEST_VARS['avancee'] = partie['est_speciale']
    REQUEST_VARS['taille'] = partie['taille']
    REQUEST_VARS['joueur'] = REQUEST_VARS['partie'][f"""nomE{REQUEST_VARS['partie']['tour']}"""]
    if partie['est_speciale']:
        None
        #REQUEST_VARS['morpions'] = recuperer_morpions(connexion, nomE)

    if POST != {}:
        print(POST['case'])
        if verifier_action(POST['case'],REQUEST_VARS['joueur'], REQUEST_VARS['grille']):
            inserer_action(connexion,partie['idP'],POST['case'])
