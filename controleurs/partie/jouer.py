from model.partie_utils import inserer_action, verifier_gagne_pos
from model.partie_simple import recompiler_partie,recuperer_partie_simple
import re

connexion = SESSION['CONNEXION']

def verifier_action_simple(grille, action):
    """
    verifie si une case est libre (partie normale)
    prends :
        - grille: tableau 2D
        - action : string "x,y"
    renvoie :
        - True si la case est libre, false sinon
    """
    pos = action.split(',')
    x=int(pos[0])
    y=int(pos[1])
    #verifie que la case est vide (0=vide)
    if grille[x][y]!=None:
        REQUEST_VARS['erreur_action']="❌ Case déjà occupée"
        return False
    return True


def verification_victoire_normale(grille, taille, equipe_joueuse):
    """
    Vérifie si l'équipe_joueuse a gagné (partie normale).
    """
    # Définition de la fonction de vérification pour l'équipe qui vient de jouer
    verif_cellule_joueuse = lambda cell: cell == equipe_joueuse

    # Vérification du placement UNIQUEMENT pour l'équipe joueuse
    if verifier_gagne_pos(grille):
        return equipe_joueuse # Renvoie 1 ou 2

    # Verifier si grille pleine
    cases_libres = sum(1 for i in range(taille) for j in range(taille) if grille[i][j] == None)
    if cases_libres == 0:
        return 'egalite'
    retur None

# Note: L'appel à select_querverifier_gagne_par_placement_equipey nécessite l'objet connexion

erreur_bool = not REQUEST_VARS.get('url_components')
erreur_bool = erreur_bool or(REQUEST_VARS['url_components'][1] == '')
# safe pour idp (il existe)
idp = REQUEST_VARS['url_components'][1]
partie = recuperer_partie_simple(connexion,idp)
erreur_bool = erreur_bool or partie == None
# à ce moment là c bizzare mais
if erreur_bool:
    REQUEST_VARS['erreur_url'] = "erreur"
else:
    if not(idp in SESSION):
        SESSION[idp] = partie

    REQUEST_VARS['partie'] = SESSION[idp]


    if POST != {}:
        if 'case' in POST:
            action=POST['case'][0]
            regexp_pos = r'[0-9],[0-9]'
            pos_ok  = re.match(regexp_pos,action)
            if pos_ok and verifier_action_simple(partie['grille'], action):
                SESSION[idp]['joueur'] = 2 if SESSION[idp]['joueur'] == 1 else 1
                SESSION[idp]['grille'][int(action[0])][int(action[2])] = SESSION[idp]['joueur']
                SESSION[idp]['gagne'] = verification_victoire_normale(SESSION[idp]['grille'],SESSION[idp]['taille'],SESSION[idp]['joueur'])
                print(SESSION[idp]['gagne'])
                inserer_action(connexion,idp,action)
        else:
            REQUEST_VARS['erreur_action']="❌ Aucune case sélectionnée"
