from model import equipe
from .utils import other_query, select_query
from model.partie_utils import init_grille
import re
import random

def verifier_gagne_elimination(morpions: list):
  """Vérifie si la liste/dict de morpions d'une équipe est vide."""
  # Accepte une liste ou un dict
  try:
    return len(morpions) == 0
  except Exception:
    return not morpions


def recuperer_partie_complexe(connexion, idp):
  """
    RENVOIE UN DICTIONNAIRE : PARTIE
  """
  query = """SELECT * FROM Partie WHERE idP = %s"""
  partie = select_query(connexion,query,[idp])

  if not partie:
    # si la requête est vide, la partie n'existe pas !
    print("Aucune partie trouvée")
    return None

  # Récupérer la ligne de la table
  row = partie[0]

  # ici on récupère les couleurs des deux équipes qui jouent
  query = 'SELECT couleurE FROM equipe WHERE nomE = %s'
  couleur1 = select_query(connexion, query, [row[1]])
  couleur2 = select_query(connexion, query, [row[2]])

  # déterminer qui doit jouer maintenant à partir du journal
  tour_row = select_query(connexion, 'SELECT MAX(numa) FROM Journal WHERE idP = %s', [idp])
  tour_val = tour_row[0][0] if tour_row and tour_row[0] else None
  if tour_val is None:
      joueur = 1
  else:
      # si le nombre d'actions est impair, c'est l'équipe 2 qui vient de jouer, donc joueur 1 joue
      joueur = 1 if (int(tour_val) % 2 == 0) else 2

  partie_dict = {
      'E1':{
        "couleur":couleur1,
        "nom":row[1],
        "morpions":recuperer_morpions_joueur(connexion,row[1])
      },
      'E2':{
        "couleur":couleur2,
        "nom":row[2],
        "morpions":recuperer_morpions_joueur(connexion,row[2])
      },
      "tour": tour_val,
      "taille": row[7] if len(row) > 6 else 3,
      "numjoueur": joueur,
      "grille":init_grille(connexion,idp)
  }
  nom_joueur_actuel = partie_dict[f"""E{partie_dict['numjoueur']}"""]['nom']
  partie_dict['morpions']= recuperer_morpions_joueur(connexion,nom_joueur_actuel)
  partie_dict['nomjoueur'] = nom_joueur_actuel
  return partie_dict

def recompiler_partie_avancee(connexion, idp):
  """
    Renvoie une grille 2D avec les morpions et leurs stats pour une partie avancée
    Recompile l'état en rejouant toutes les actions du journal
  """

def recuperer_morpions_joueur(connexion, nom_equipe):
  """
  Récupère les morpions disponibles pour une équipe dans une partie
  """
  query = """SELECT m.idM, m.nomM, m.image, m.PV, m.ATK, m.MANA, m.REU,p.nomE
        FROM Morpion m JOIN Posseder p ON p.idM = m.idM
        WHERE p.nomE=%s"""
  morpions = select_query(connexion, query, [nom_equipe])
  liste_morpions = [{
                'id':m[0],
                'image': m[2],
                'PV': m[3],
                'ATK': m[4],
                'MANA': m[5],
                'REU': m[6],
                'nomE':m[7]}for m in morpions]

  return liste_morpions
