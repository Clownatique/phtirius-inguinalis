from model import equipe
from .utils import other_query, select_query

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


def recompiler_partie(connexion, idP):
  """
    Renvoie un tableau correspondant à la partie passé en paramètre
  """
  sel_partie = """WHERE idp = %s"""
  query = f"""SELECT * FROM journal {sel_partie} ORDER BY numA DESC"""
  actions = select_query(connexion,query, [idP])
  query = """SELECT taille_grille FROM partie """+sel_partie
  taille_grille = select_query(connexion, query,[idP])[0][0]
  print(f'''action joué durant la partie {idP}:{actions}''')
  if taille_grille == None:
    taille_grille = 3

  grille = [[0 for _ in range(taille_grille)] for _ in range(taille_grille)]
  # 0 : case vide
  # None : case détruite
  # 'idM' : morpion avancé dessus
  # 1/2 : partie simple

  for i in actions:
    # une action dans le contexte d'une partie simple ça ressemble à ça:
    # (0 ou 1): x,y
    # pour l'instant les grilles ne peuvent pas aller au dessus de 9
    print(f"action:{i}")
    x = int(i[1][:1])
    y = int(i[1][2:])
    grille[x][y] = 1 if i[0] % 2 != 0 else 2

  return grille

def recuperer_partie(connexion, idp):
  """
    RENVOIE UN DICTIONNAIRE : PARTIE
  """
  query = """SELECT * FROM Partie WHERE idP = %s"""
  partie = select_query(connexion,query,[idp])

  if len(partie) == 0:
    # si la requête est vide, la partie n'existe pas !
    return 404
  else:
    # ici on récupère les couleurs des deux équipes qui jouent
    query = '''SELECT couleure FROM equipe WHERE nomE = %s'''
    couleur = [select_query(connexion, query,[partie[0][i]])[0][0] for i in range(1,3)]

    tour = select_query(connexion,'SELECT MAX(numa) FROM Journal WHERE idp = %s',[idp])
    # ici on récupère le numéro de l'équipe qui doit jouer
    if tour[0][0] == None:
      tour = 1
    elif type(tour[0][0]) == int:
      tour = 2 if (tour[0][0] % 2 != 0) else 1

    # if idp in SESSION:
      # grille = SESSION[idp]
    # else:
    grille = recompiler_partie(connexion,idp)
      # SESSION[idp] = grille

    partie = {
      "nomE1":partie[0][1],
      "couleurE1": couleur[0],
      "nomE2":partie[0][2],
      "couleurE2": couleur[1],
      "idP":idp,
      "tour":tour,
      "grille":grille,
      "taille":partie[0][6],
      "est_speciale":partie[0][7]
    }
    return partie

def inserer_action(connexion, idPartie:int, action):
  requete_numa = "SELECT max(numa)+1 FROM Journal WHERE idp = %s"
  numa = select_query(connexion,requete_numa,[idPartie])[0][0]
  if numa == None:
    numa = 1
  else:
    numa = int(numa)
  print(action)
  requete = """INSERT INTO JOURNAL (numa, idP, texte_action,date_action) VALUES (%s,%s,%s,NOW())"""
  valeurs = [numa, idPartie,action[0]]
  return other_query(connexion, requete, valeurs)


def creer_partie(connexion, nomE1, nomE2, est_special,max_tours,taille_grille):
    sql = """INSERT INTO PARTIE (nomE1, nomE2, date_debut, est_speciale,max_tours,taille_grille)
          VALUES (%s, %s, NOW(), %s, %s, %s)"""
    print(sql)
    valeurs=[nomE1, nomE2, est_special,max_tours,taille_grille]
    idP = other_query(connexion, sql, valeurs)
    return idP
