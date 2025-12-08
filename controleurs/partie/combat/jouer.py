from model.partie import inserer_action, terminer_partie
from model.partie_complique import recompiler_partie_avancee, recuperer_morpions_joueur, recuperer_partie_complexe
from model.partie_utils import verifier_gagne_pos
import re

connexion = SESSION['CONNEXION']

#pyright: reportUndefinedVariable=false
#

def gagne(partie):
    grille = partie['grille']
    nom_joueur = partie['nomjoueur']
    num_adversaire = 1 if partie['numjoueur'] == 2 else 2
    nom_adversaire = partie[f"""E{num_adversaire}"""]
    morpions = partie['morpions']

    if len(morpions) == 0:
        return partie[f"""E{num_adversaire}"""]['nom']#autre joueur

    print(grille)

    grille_pr_verif = []
    for lignes in grille:
        ligne = []
        for mor in lignes:
            if mor == None:
                ligne.append(False)
            elif 'nomE' in mor and mor['nomE'] == nom_joueur:
                ligne.append(True)
            else:
                ligne.append(False)
            #pas d'autre exceptions en vue
        grille_pr_verif.append(ligne)
    print(grille_pr_verif)

    if verifier_gagne_pos(grille_pr_verif):
        return nom_joueur

    case_restante = bool()

    for ligne in grille:
        for mor in ligne:
            if mor == None:
                case_restante = False
                break
    # if partie['tour'] > partie['maxtour'] or case_restante:
        # return 'égalité'


def jouer_coup(partie, action):
  """Applique une action simple à la partie en mémoire (placements et sorts basiques).
  Ne persiste pas la partie. Retourne la partie modifiée."""
  coup = action
  grille = partie.get('grille', [])
  morpions = partie.get('morpions', [])
  joueur_actuel = partie['numjoueur']
  num_adversaire = 1 if partie['numjoueur'] == 2 else 2
  indice = 0 if joueur_actuel == 1 else 1
  morpions_du_joueur = morpions[indice] if morpions and len(morpions) > indice else {}

  if coup[0].isalpha():
    # sorts (format attendu ex: 'at:1,2>2,2' ou 'bf:1,2>2,2')
    if coup[1:] == '-':
      # échec du sort
      return partie

    # extraire nombres
    acteur = grille[int(action[3])][int(action[5])]
    cible = grille[int(action[7])][int(action[9])]

    sort = coup[:2]
    if sort == 'at' and acteur and cible:
      cible['PV'] -= acteur.get('ATK', 0)
    elif sort == 'bf' and cible:
      cible['PV'] -= 3
      cible['MANA'] -= 2
    elif sort == 'sn' and cible:
      cible['PV'] += 1
      cible['MANA'] += 1
    elif sort == 'ag' and acteur:
      # ag détruit la cible si présente
      cible = "détruit"
      acteur['MANA'] -= 5

    print(f"cible:{cible}")

      # supprimer la cible si plus de PV
    if type(cible) == dict:
      if cible['PV']<0:
        grille[cx][cy] = None

    grille[int(action[3])][int(action[5])] = acteur
    grille[int(action[7])][int(action[9])] = cible

  else:
    # placement classique attendu: 'x,y<id' (ex: '1,2<3') ou déjà 'x,y'
    print("placement détecté")
    if '<' in coup:
      coords, id_part = coup.split('<')
      x_str, y_str = coords.split(',')
      x = int(x_str.strip())
      y = int(y_str.strip())
      for morpion in morpions:
        if morpion['id'] == int(id_part):
          morpion = morpions.pop(morpions.index(morpion))
          grille[x][y] = morpion
          partie[f"""E{joueur_actuel}"""]['morpions'] = morpions
          break #pcq va pas

  print(f"""fin fonction jouer coup:{coup}""")
  partie['grille'] = grille
  partie['numjoueur'] = 1 if partie['nomjoueur'] == 2 else 2
  # partie['nomjoueur'] = partie[f"""E{partie['numjoueur']}"""]['nomE']
  print(partie[f"""E{partie['numjoueur']}"""])
  partie['morpions'] =partie[f"""E{num_adversaire}"""]['morpions']
  return partie


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
        # SESSION[idp]= recompiler_partie_avancee(connexion,idp)
        # partie=SESSION[idp]
        SESSION['partie'] = recuperer_partie_complexe(connexion,idp)
    # + recompilation si nécessaire
    REQUEST_VARS['partie'] = SESSION['partie']
    partie = REQUEST_VARS['partie']
    print(partie)
    # REQUEST_VARS['partie'] = partie
    # REQUEST_VARS['nomEJ'] = partie[f"nomE{partie['joueur']}"]
    # nom de l'équipe qui joue nécessaire

    if POST != {}:
        if 'case' in POST:
            #d'abord on vérifie si l'action c un placement
            if 'action' in POST:
                case = POST['case'][0]
                action = POST['action'][0]
                if not(action[0].isalpha()):
                    # donc c un placement dans partie avancé car pas de sorts
                    action = f"{case}<{action}"
                else:
                    action = f"{action}>{case}"


                regexp_sort = r'(sn|bf|ag|at):([0-9],[0-9])<([0-9],[0-9])'
                regexp_pos = r'[0-9],[0-9]<[0-9]+'

                sort_ok = re.match(regexp_sort,action)
                pos_ok  = re.match(regexp_pos,action)
                print(f"""les tests:{sort_ok} {pos_ok}""")
                print(f"action:{action}")
                if  pos_ok != None or sort_ok != None:
                    SESSION[idp] = jouer_coup(partie, action)
                    REQUEST_VARS['partie'] = SESSION[idp]
                    if gagne(partie):
                        inserer_action(connexion,idp, action)
                        terminer_partie(connexion,idp,gagne(partie))
                        SESSION[idp]["gagne"] = True

                else:
                    print('que ça bidouille')
        else:
            REQUEST_VARS['erreur_action']="❌ Aucune case sélectionnée"
    else:
        REQUEST_VARS['erreur_action'] = "aucune action"
