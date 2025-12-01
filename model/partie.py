from psycopg import sql
from datetime import datetime
from .utils import other_query, select_query
from .partie_nestor import recuperer_partie
from .partie_flora import recompiler_partie


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
