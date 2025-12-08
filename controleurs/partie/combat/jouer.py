from model.utils import select_query
from model.partie import inserer_action, terminer_partie, verifier_gagne_pos, recuperer_partie, inserer_action_complexe, creer_partie, init_grille, recompiler_partie, verifier_action
from model.partie_complique import recompiler_partie_avancee, recuperer_morpions_joueur, recuperer_partie_complexe, verifier_gagne_elimination
import re


connexion = SESSION['CONNEXION']

#pyright: reportUndefinedVariable=false

def verifier_gagne_elimination(morpions: list):
  """Vérifie si la liste/dict de morpions d'une équipe est vide."""
  # Accepte une liste ou un dict
  test = [True if morpion['PV']<0 else False for morpion in morpions]
  return all(test)

def jouer_coup(partie, action):
    grille = partie.get('grille', [])
    morpions = partie.get('morpions', [])
    joueur_actuel = partie['numjoueur']
    num_adversaire = 1 if partie['numjoueur'] == 2 else 2
    indice = 0 if joueur_actuel == 1 else 1
    morpions_du_joueur = morpions[indice] if morpions and len(morpions) > indice else {}

    # Vérification si l'action est un sort ou un placement
    if ':' in action:
        # Sort
        coup = action
        acteur = grille[int(coup[3])][int(coup[5])]
        cible = grille[int(coup[7])][int(coup[9])]
        sort = coup[:2]
        # reussite
        #

        if sort == 'at' and acteur and cible:
            cible['PV'] -= acteur['ATK']

        elif sort == 'bf':
            cible['PV'] =- 3
            acteur['MANA'] =- 2

        elif sort == 'ag' and acteur:
            cible = "détruit"
            acteur['MANA'] -= 5

        elif sort == 'sn' and acteur and cible:
            cible['PV'] =+1
            acteur['MANA'] =-1
        else:
            pass

        # Suppression de la cible si plus de PV
            if type(cible) == dict and cible['PV'] < 0:
                cible = None

            grille[int(coup[3])][int(coup[5])] = acteur
            grille[int(coup[7])][int(coup[9])] = cible

    else:
        # Placement classique
        print("placement détecté")
        if '<' in action:
            coords, id_part = action.split('<')
            x_str, y_str = coords.split(',')
            x, y = int(x_str.strip()), int(y_str.strip())
            for morpion in morpions:
                if morpion['id'] == int(id_part):
                    morpion = morpions.pop(morpions.index(morpion))
                    grille[x][y] = morpion
                    partie[f"E{joueur_actuel}"]['morpions'] = morpions
                    break

    # Mise à jour de la partie
    partie['numjoueur'] = 1 if partie['numjoueur'] == 2 else 2
    partie['morpions'] = partie[f"E{num_adversaire}"]['morpions']
    return partie

def verifier_action(action:str, grille:list) -> bool|str:
    """
        renvoie True quand c bon
    """
    regexp_sort = r'(sn|bf|ag|at):([0-9],[0-9])>([0-9],[0-9])'
    regexp_pos = r'[0-9],[0-9]<[0-9]+'
    sort_ok = re.match(regexp_sort,action)
    pos_ok  = re.match(regexp_pos,action)

    if pos_ok:
        case = grille[int(action[0])][int(action[0])]
        return (case == None or case != "détruit","vous devez mettre le morpion sur une case qui vide!")
    if sort_ok:
        morpion = grille[int(action[3])][int(action[5])]
        morpion_acteur = grille[int(action[7])][int(action[9])]
        if action[-2:] == 'ag':
            return (action[3] != action[7] and action[5] != action[9],"pas de kamikaze dans ce jeu ! cf sujet")
        return (not(morpion == None or morpion == "détruit" or morpion_acteur == None or morpion['nomE'] == morpion_acteur['nomE']), "vous devez viser un morpion, et un morpion de l'équipe adverse !")
    return (True,"")

erreur_bool = not REQUEST_VARS.get('url_components')
erreur_bool = erreur_bool or(REQUEST_VARS['url_components'][0] == '')
if erreur_bool:
    REQUEST_VARS['erreur'] = "erreur"
else:

    # SAUVEGARDE PARTIE => SESSION
    idp = REQUEST_VARS['url_components'][1]
    if idp == None:
        idp = 0
    if idp in SESSION:
        partie = SESSION[idp]
    else:
        partie = recuperer_partie_complexe(connexion,idp)
        SESSION[idp] = partie
    # + recompilation si nécessaire
    REQUEST_VARS['partie'] = partie

    #
    # REQUEST_VARS['partie'] = partie
    # REQUEST_VARS['nomEJ'] = partie[f"nomE{partie['joueur']}"]
    # nom de l'équipe qui joue nécessaire

    if POST != {}:

        partie = REQUEST_VARS['partie']
        if 'case' in POST and 'action' in POST:
            case = POST['case'][0]
            action = POST['action'][0]
            if not(action[0].isalpha()):
                # donc c un placement dans partie avancé
                action = f"{case}<{action}"
            else:
                action = f"{action}>{case}"

            grille = SESSION[idp]

            verif= verifier_action(action, SESSION[idp]['grille'])

            if verif[0] == True:
                SESSION[idp] = jouer_coup(partie, action)
                REQUEST_VARS['partie'] = SESSION[idp]
                adverse = 1 if SESSION[idp]['numjoueur'] == 2 else 2
                pour_verif = init_grille(connexion,idp)

                grille_pour_verif = []
                for ligne in SESSION[idp]['grille']:
                    ligne_verif = []
                    for morpion in ligne:
                        if morpion is None or SESSION[idp][f"E{adverse}"]['nom'] is None:
                            ligne_verif.append(False)
                        else:
                            ligne_verif.append(morpion['nomE'] == SESSION[idp][f"E{adverse}"]['nom'])
                    grille_pour_verif.append(ligne_verif)

                SESSION[idp]['gagne'] = verifier_gagne_pos(grille_pour_verif) or verifier_gagne_elimination(SESSION[idp]['morpions'])

                inserer_action(connexion,idp, action)

            else:
                REQUEST_VARS['erreur'] = verif[1]
        else:
            REQUEST_VARS['erreur_action']="❌ Aucune case sélectionnée"
