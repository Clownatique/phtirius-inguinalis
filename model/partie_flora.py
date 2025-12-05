from psycopg import sql
from datetime import datetime
from model.utils import other_query, select_query


def recompiler_partie(connexion, idP):
  """
    Renvoie un tableau 2D correspondant à une partie normale
  """
  #récupère toutes les actions :
  sel_partie="""WHERE idP = %s"""
  query = f"""SELECT numA, texte_action FROM journal {sel_partie} ORDER BY numA ASC"""
  actions = select_query(connexion,query, [idP])

  #récupère la taille de la grille :
  query_taille = """SELECT taille_grille FROM partie """+sel_partie
  info_partie = select_query(connexion, query_taille,[idP])
  taille_grille = info_partie[0][0] if info_partie else 3



  #initialisation de la grille vide
  grille = [[0 for _ in range(taille_grille)] for _ in range(taille_grille)]
  # 0 : case vide
  # None : case détruite
  # 1 = equipe 1, 2 = équipe 2

  #rejouer toutes les actions
  for a in actions:
    numa=a[0]
    texte=a[1]
    try:
      #on cherche un pattern "x,y"
      if ',' in texte:
        parties = texte.split(',')
        # Extraire les chiffres
        x = int(parties[0][-1])  # Dernier caractère avant la virgule
        y = int(parties[1][0])   # Premier caractère après la virgule

        # Déterminer quelle équipe (1 ou 2)
        equipe = 1 if (numa % 2 != 0) else 2
        grille[x][y] = equipe
    except Exception as e:
      print(f"Erreur parsing action {numa}: {texte} - {e}")
  return grille

def recompiler_partie_avancee(connexion, idP):
  """
    Renvoie une grille 2D avec les morpions et leurs stats pour une partie avancée
    Recompile l'état en rejouant toutes les actions du journal
  """
  #récupère la taille de la grille et les équipes
  query_partie="""SELECT taille_grille, nomE1, nomE2 FROM partie WHERE idp = %s"""
  info_partie=select_query(connexion, query_partie, [idP])
  taille_grille=info_partie[0][0] if info_partie else 3
  nomE1=info_partie[0][1]
  nomE2=info_partie[0][2]

  #initialisation de la grille vide
  # None = case vide, dict = morpion ou case détruite
  grille=[[None for _ in range(taille_grille)] for _ in range(taille_grille)]

  #récupère tous les morpions disponibles pour chaque équipe
  query_morpions= """
        SELECT m.idM, m.nomM, m.image, m.PV, m.ATK, m.MANA, m.REU, p.nomE
        FROM Morpion m JOIN Posseder p ON m.idM=p.idM
        WHERE p.nomE IN (%s, %s)
        """
  morpions_disponibles=select_query(connexion, query_morpions, [nomE1, nomE2])

  #crée un dictionnaire des morpions
  morpions_dict={}
  for m in morpions_disponibles:
    morpions_dict[m[0]]={
      'nomM':m[1],
      'image':m[2],
      'PV':m[3],
      'ATK':m[4],
      'MANA':m[5],
      'REU':m[6],
      'equipe':m[7],
      #stats actuelles (évoluent durant la partie)
      'PV_actuel':m[3],
      'MANA_actuel':m[5],
      'REU_actuel':float(m[6]),
      'est_vivant':True,
      'position_x':None,
      'position_y':None
    }

  #récupère toutes les actions du journal
  query_actions="""
                SELECT numa, texte_action, type_action
                FROM Journal
                WHERE idp=%s
                ORDER BY numa ASC
                """
  actions=select_query(connexion, query_actions, [idP])

  #rejouer toutes les actions pour reconstruire l'état
  print(f"morpions:{morpions_dict}")
  for a in actions:
    print(actions)
    numa=a[0]
    texte=a[1]
    print(texte[:3])
    print(texte[:3].isalnum())

    if not(texte[:3].isalnum()):
      print("c'est bien un placement")
      morpion = texte[5:]
      grille[int(texte[0])][int(texte[2])] = morpions_dict[int(morpion)]
    else:
      sort = texte[3:]

  print(grille)

  return grille

def recuperer_morpions_joueur(connexion, idp, nom_equipe):
  """
  Récupère les morpions disponibles pour une équipe dans une partie
  """
  query = """
        SELECT m.idM, m.nomM, m.image, m.PV, m.ATK, m.MANA, m.REU
        FROM Morpion m JOIN Posseder p ON p.idM = m.idM
        WHERE p.nomE=%s
    """
  morpions = select_query(connexion, query, [nom_equipe])

  morpions_list = []
  for m in morpions:
    morpions_list.append({
      'idM': m[0],
      'nomM': m[1],
      'image': m[2],
      'PV': m[3],
      'ATK': m[4],
      'MANA': m[5],
      'REU': m[6],
      'PV_actuel': m[3],
      'MANA_actuel': m[5],
      'REU_actuel': float(m[6]),
      'position_x': None,
      'position_y': None,
      'est_vivant': True
       })

  return morpions_list

def verifier_action(grille, action):
  # coup illégal : placer un pion alors qu'il y'en a déjà un
  try :
    x, y=action.split(',')
    x=int(x)
    y=int(y)
    case=grille[x][y]

    #partie normale: une case libre vaut 0
    if case==0:
      return True

    #partie avancée: une case libre vaut None
    elif case is None:
      return True

    else:
      return False

  except Exception as e:
    print(f"Erreur vérification action: {e}")
    return False

def creer_texte_action(type_action, **params):
  """
  génère le texte_action formaté

  exemples :
  creer_texte_action('placement', idM=1, x=0, y=1)
  creer_texte_action('attaque', attaquant=1, cible_x=2, cible_y=1)
  creer_texte_action('sort_feu', lanceur=3, cible_x=1, cible_y=2)
  """
  if type_action == 'placement':
    return f"idM:{params['idM']};x:{params['x']};y:{params['y']}"

  elif type_action == 'attaque':
    return f"attaque;attaquant:{params['attaquant']};cible_x:{params['cible_x']};cible_y:{params['cible_y']}"

  elif type_action == 'sort_feu':
    return f"sort:feu;lanceur:{params['lanceur']};cible_x:{params['cible_x']};cible_y:{params['cible_y']}"

  elif type_action == 'sort_soin':
    return f"sort:soin;lanceur:{params['lanceur']};cible:{params['cible']}"

  elif type_action == 'sort_armageddon':
    return f"sort:armageddon;x:{params['x']};y:{params['y']}"

  else :
    return str(params)
