from psycopg import sql
from datetime import datetime
from .utils import other_query, select_query

def liste_equipe(connexion):
  None

def recompiler_partie(connexion, partie:list):
  """
    Renvoie un tableau correspondant à la partie passé en paramètre
  """
  sel_partie = """WHERE nomE1 = '%s', couleurE1 = '%s', nomE2 = '%s', couleurE2 = '%s', date = %s"""
  partie_args = [partie[0],partie[1],partie[2],partie[3],partie[4]]

  query = """SELECT action FROM journal ORDER BY action DESC""" + sel_partie
  actions = select_query(connexion,query, partie_args)

  query = """SELECT taille_grille FROM partie"""+sel_partie
  taille_grille = select_query(connexion, query,partie_args)

  partie = [[0 for _ in range(taille_grille)] for _ in range(taille_grille)]

  for i in actions:
    case = i


def verifier_action(connexion, partie, action):
  None

def update_possesion(connexion, equipe, morpion):
  None

def inserer_action(connexion, partie, action):
  None



def creer_partie(connexion, nomE1, couleurE1, nomE2, couleurE2):
  try :
    cur=connexion.cursor()
    sql = """INSERT INTO PARTIE (couleurE1, nomE1, couleurE2, nomE2, date_debut, est_special)
          VALUES (%s, %s, %s, %s, %s, %s)
          RETURNING idP;"""
    valeurs=(couleurE1, nomE1, couleurE2, nomE2, datetime.now(), est_special)
    cur.execute(sql,valeurs)
    idP=cur.fetchone()[0]
    connexion.close()
    cur.close()
    return idP
  except psycopg.Error as e:
    return e

def creer_partie(connexion,nomE1,couleurE1,nomE2,couleurE2):
  query = """"""
  query = """INSERT INTO PARTIE values (couleurE1, nomE1, couleurE2, nomE2, date_debut, est_special)
          VALUES (%s, %s, %s, %s, %s, %s)
          RETURNING idP;"""
  valeurs = [couleurE1, nomE1, couleurE2]
