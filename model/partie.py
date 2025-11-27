from psycopg import sql
from datetime import datetime
from .utils import other_query, select_query

def recuperer_partie(connexion, idp):
  """
    RENVOIE UN DICTIONNAIRE : PARTIE
  """
  query = """SELECT * FROM Partie WHERE idP = %s"""
  partie = select_query(connexion,query,[idp])

  if len(partie) == 0:
    print("aucune partie trouvé")
    return 404
  else:
    query = '''SELECT couleure FROM equipe WHERE nomE = %s'''

    print(partie)
    #select_query(connexion, query,[partie[0][i]])

    couleur = [select_query(connexion, query,[partie[0][i]])[0][0] for i in range(1,3)]

    tour = select_query(connexion,'SELECT MAX(numa) FROM Journal WHERE idp = %s',[idp])

    if tour[0][0] == None:
      tour = 1
    elif type(tour[0][0]) == int:
      tour = 2 if (tour[0][0] % 2 != 0) else 1

    partie = {
      "nomE1":partie[0][1],
      "couleurE1": couleur[0],
      "nomE2":partie[0][2],
      "couleurE2": couleur[1],
      "idP":idp,
      "tour":tour,
      "taille":partie[0][6],
      "est_speciale":partie[0][7]
    }
    return partie

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

  for i in actions:
    # une action dans le contexte d'une partie simple ça ressemble à ça:
    # (0 ou 1): x,y
    # pour l'instant les grilles ne peuvent pas aller au dessus de 9
    x = int(i[2][:1])
    y = int(i[2][2:])
    grille[x][y] = 1 if i[0] % 2 != 0 else 2

  return grille

def verifier_action(connexion, grille:list, action):
  # coup illégal : placer un pion alors qu'il y'en a déjà un
  x = action[2:-2]
  y = action[4:]
  if partie['grille'][x][y]:
    return False
  return True

def inserer_action(connexion, idPartie:int, action):
  requete = """INSERT INTO JOURNAL (idP, texte_action,date_action) VALUES (%s,%s,NOW())"""
  valeurs = [idPartie,action]
  return other_query(requete, valeurs)


def creer_partie(connexion, nomE1, couleurE1, nomE2, couleurE2,est_special):
    sql = """INSERT INTO PARTIE (couleurE1, nomE1, couleurE2, nomE2, date_debut, est_special)
          VALUES (%s, %s, %s, %s, %s, %s) RETURNING idP;"""
    valeurs=(couleurE1, nomE1, couleurE2, nomE2, datetime.now(), est_special)
    idP = other_query(connexion, sql, valeurs)
    return idP
