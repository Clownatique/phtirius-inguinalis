from model.partie import inserer_action, terminer_partie, verifier_gagne_pos, recuperer_partie, inserer_action_complexe, creer_partie, init_grille, recompiler_partie, verifier_action
from model.partie_complique import recompiler_partie_avancee, recuperer_morpions_joueur, recuperer_partie_complexe, verifier_gagne_elimination
import re


connexion = SESSION['CONNEXION']

#pyright: reportUndefinedVariable=false

def jouer_coup(partie, action):
  """Applique une action simple à la partie en mémoire (placements et sorts basiques).
  Ne persiste pas la partie. Retourne la partie modifiée."""
  coup = action
  grille = partie.get('grille', [])
  morpions = partie.get('morpions', [])
  joueur_actuel = partie['numjoueur']
  indice = 0 if joueur_actuel == 1 else 1
  morpions_du_joueur = morpions[indice] if morpions and len(morpions) > indice else {}

  if coup[0].isalpha():
    # sorts (format attendu ex: 'at:1,2>2,2' ou 'bf:1,2>2,2')
    if coup[1:] == '-':
      # échec du sort
      return partie

    # extraire nombres
    acteur = grille[ax][ay]
    cible = grille[ax][ay]

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
      if cible:
        grille[cx][cy] = None
        acteur['MANA'] -= 5

      # supprimer la cible si plus de PV
      if cible['PV'] <= 0:
        grille[cx][cy] = None


  else:
    # placement classique attendu: 'x,y<id' (ex: '1,2<3') ou déjà 'x,y'
    print("placement détecté")
    if '<' in coup:
      coords, id_part = coup.split('<', 1)
      x_str, y_str = coords.split(',', 1)
      x = int(x_str.strip())
      y = int(y_str.strip())
      for morpion in morpions:
        if morpion['id'] == int(id_part):
          print(morpion)
          grille[x][y] = morpions.pop(morpions.index(morpion))
          partie[f"""E{joueur_actuel}"""]['morpions'] = morpions
          break #pcq va pas

  print(f"""fin fonction jouer coup:{coup}""")
  partie['grille'] = grille
  partie['numjoueur'] = 1 if partie['nomjoueur'] == 2 else 2
  # partie['nomjoueur'] = partie[f"""E{partie['numjoueur']}"""]['nomE']
  print(partie[f"""E{partie['numjoueur']}"""])
  partie['morpions'] =partie[f"""E{partie['numjoueur']}"""]['morpions']
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
                    # donc c un placement dans partie avancé
                    action = f"{case}<{action}"
                else:
                    action = f"{action}>{case}"


                regexp_sort = r'(sn|bf|ag|at):([0-9],[0-9])(<|>)([0-9],[0-9])'
                regexp_pos = r'[0-9],[0-9]<[0-9]+'

                sort_ok = re.match(regexp_sort,action)
                pos_ok  = re.match(regexp_pos,action)
                print(f"""les tests:{sort_ok} {pos_ok}""")
                print(f"action:{action}")
                if  pos_ok != None or sort_ok != None:
                    SESSION[idp] = jouer_coup(partie, action)
                    REQUEST_VARS['partie'] = SESSION[idp]
                    inserer_action(connexion,idp, action)
                else:
                    print('que ça bidouille')
        else:
            REQUEST_VARS['erreur_action']="❌ Aucune case sélectionnée"
    else:
        REQUEST_VARS['erreur_action'] = "aucune action"
