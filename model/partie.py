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
    print("résultat de la requête:")

    print(partie)
    partie = {
    "nomE1":partie[1],
    "nomE2":partie[2],
      "idP":idp,
      "taille_grille":partie[6],
    }
    return partie
  else:
    print(partie)
    print(partie[0])
    print("la requete renvoie plus de 0 instances")


def recompiler_partie(connexion, partie:list):
  """
    Renvoie un tableau correspondant à la partie passé en paramètre
  """
  sel_partie = """WHERE nomE1 = '%s', couleurE1 = '%s', nomE2 = '%s', couleurE2 = '%s', date = %s"""
  partie_args = [partie[0],partie[1],partie[2],partie[3],partie[4]]
  query = """SELECT * FROM journal ORDER BY action DESC""" + sel_partie
  actions = select_query(connexion,query, partie_args)
  query = """SELECT taille_grille FROM partie"""+sel_partie
  taille_grille = select_query(connexion, query,partie_args)

  grille = [[None for _ in range(taille_grille)] for _ in range(taille_grille)]

  for i in actions:
    # une action dans le contexte d'une partie simple ça ressemble à ça:
    # (0 ou 1): x,y
    # pour l'instant les grilles ne peuvent pas aller au dessus de 9
    x = i[2:-2]
    y = i[4:]
    grille[x][y] = i[:1]

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
