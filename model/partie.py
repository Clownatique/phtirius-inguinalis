from model import equipe
from .utils import other_query, select_query

def terminer_partie(connexion, idP,gagnant):
    query = """UPDATE Partie SET est_terminee = TRUE, date_fin = NOW(),
nomE_gagnant = %s WHERE idP = %s"""
    other_query(connexion, query, [gagnant, idP])
    # Ajouter une entrée dans le journal
    query_journal ="""
INSERT INTO Journal (numa, idP, texte_action, date_action, type_action)SELECT
COALESCE(MAX(numa), 0) + 1, %s, %s, NOW(), 'victoire'FROM Journal WHERE idP = %s """
    texte = f"Victoire de {gagnant}" if gagnant != 'egalite' else "Égalité"
    other_query(connexion, query_journal, [idP, texte, idP])

def recup_equipe(connexion, nome):
  query = 'SELECT nomm, image,PV,ATK,MANA,REU FROM Morpion m JOIN Equipe e USING WHERE e.nome = %s'
  equipe_morpions = select_query(connexion, query, [nome])
  morpions = dict()
  for morpion in equipe_morpions[0]:
    morpions[morpion[0]] = {
      'nom':morpion[0],
      'image':morpion[1],
      'PV':morpion[2],
      'ATK':morpion[3],
      'MANA':morpion[4],
      'REU':morpion[5],
    }
  return morpions

def recuperer_partie(connexion, idp):
  """
    RENVOIE UN DICTIONNAIRE : PARTIE
  """
  query = """SELECT * FROM Partie WHERE idP = %s"""
  partie = select_query(connexion,query,[idp])

  if not partie:
    # si la requête est vide, la partie n'existe pas !
    print("Aucune partie trouvée")
    return None
  else:
    # ici on récupère les couleurs des deux équipes qui jouent
    query = '''SELECT couleurE FROM equipe WHERE nomE = %s'''
    couleur = [select_query(connexion, query,[partie[0][i]])[0][0] for i in range(1,3)]

    tour = select_query(connexion,'SELECT MAX(numa) FROM Journal WHERE idp = %s',[idp])
    # ici on récupère le numéro de l'équipe qui doit jouer
    if tour[0][0] == None:
      tour = 1
    else :
      tour = 2 if (tour[0][0] % 2 != 0) else 1

    partie = {
      "nomE1":partie[0][1],
      "couleurE1": couleur[0],
      "nomE2":partie[0][2],
      "couleurE2": couleur[1],
      "idP":idp,
      "tour":tour,
      "taille":partie[0][6],
      "max_tours":partie[0][5],
      "est_speciale":partie[0][7]
    }
    return partie

def inserer_action_complexe(connexion,idp,action):
    proba=reu_actuel*10
    tirage=random.randint(0,100)
    if tirage<proba:
      action=action+'/'
    else:
      action=action+str(r"\")

def inserer_action(connexion, idPartie:int, action):
  """
  Insère une action dans le journal
  action = texte de l'action
  """
  #récupère le prochain numéro d'action
  requete_numa = "SELECT max(numa) FROM Journal WHERE idp = %s"
  numa = select_query(connexion,requete_numa,[idPartie])[0][0]
  if numa is None:
    numa = 1
  else:
    numa = int(numa)+1

  requete = """INSERT INTO JOURNAL (numa, idP, texte_action,date_action, type_action) VALUES (%s,%s,%s,NOW(), 'placement')"""
  valeurs = [numa, idPartie,action]
  return other_query(connexion, requete, valeurs)


def creer_partie(connexion, nomE1, nomE2, est_special,max_tours,taille_grille):
    sql = """INSERT INTO PARTIE (nomE1, nomE2, date_debut, est_speciale,max_tours,taille_grille)
          VALUES (%s, %s, NOW(), %s, %s, %s)"""

    valeurs=[nomE1, nomE2, est_special,max_tours,taille_grille]
    idP = other_query(connexion, sql, valeurs)
    return idP
from psycopg import sql
from datetime import datetime
from model.utils import other_query, select_query


def recuperer_partie(connexion, idp) -> tuple:
  sel_partie="""WHERE idP = %s"""
  query = f"""SELECT numA, texte_action FROM journal {sel_partie} ORDER BY numA ASC"""
  actions = select_query(connexion,query, [idP])

  #récupère la taille de la grille :
  query_taille = """SELECT taille_grille FROM partie """+sel_partie
  info_partie = select_query(connexion, query_taille,[idP])
  taille_grille = info_partie[0][0] if info_partie else 3

  #initialisation de la grille vide
  grille = [[None for _ in range(taille_grille)] for _ in range(taille_grille)]
  return (grille,actions)

def jouer_sort(grille,sort:str) -> tuple|bool:
    """
        renvoie le tuple du sort si c un sort
        false le cas échéant
        sort
    """
    if sort[1:] == '\':
      return grille
    sort = sort[:2]
    acteur = grille[sort[3]][sort[5]]
    cible = grille[sort[7]][sort[9]]
    if sort == "at":
       cible['PV'] =- acteur['ATK']
    elif sort == "bf":
      cible['PV'] =-3
      cible['MANA'] =-2
    elif sort == 'sn':
      cible['PV'] =+1
      cible['MANA'] =1
    elif sort == 'ag':
      cible = None # à revoir pcq c pas comme ça qu'on détruit une case proprement
      acteur['MANA'] =-5
    else:
      return grille

def recompiler_partie(connexion, idP):
  """
    Renvoie un tableau 2D correspondant à une partie normale
  """
  grille_actions = recuperer_partie(connexion, idp)
  grille = grille_actions[0]
  actions = grille_actions[1]

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

  grille_actions = recuperer_partie(connexion, idp)
  grille = grille_actions[0]
  actions = grille_actions[1]
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
    }

  #récupère toutes les actions du journal
  for action in actions:
    if action[0].isalpha() and action[1].isalpha():
      grille = jouer_sort(grille,sort)
    else:
      idM = action[3:]
      grille[action[0]][action[1]] = morpions_dict[idM]
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
    if case==None:
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
