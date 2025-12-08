from .utils import select_query, other_query
from model.partie_utils import init_grille

def recuperer_partie_simple(connexion,idp):
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
  couleur = [couleur1[0][0] if couleur1 else None, couleur2[0][0] if couleur2 else None]

  # déterminer qui doit jouer maintenant à partir du journal
  tour_row = select_query(connexion, 'SELECT MAX(numa) FROM Journal WHERE idP = %s', [idp])
  tour_val = tour_row[0][0] if tour_row and tour_row[0] else None
  if tour_val is None:
      joueur = 1
  else:
      # si le nombre d'actions est impair, c'est l'équipe 2 qui vient de jouer, donc joueur 1 joue
      joueur = 1 if (int(tour_val) % 2 == 0) else 2

  partie_dict = {
      "nomE1": row[1],
      "couleurE1": couleur[0],
      "nomE2": row[2],
      "couleurE2": couleur[1],
      "tour": tour_val,
      "taille": row[7] if len(row) > 6 else 3,
      "max_tours": row[5] if len(row) > 5 else None,
      "est_speciale": row[8] if len(row) > 7 else False,
      "joueur": joueur,
  }

  # Fournir une grille par défaut (vide) pour éviter les erreurs côté template
  partie_dict['grille'] = init_grille(connexion,idp)
  joueur_actuel = partie_dict['nomE1'] if partie_dict['joueur'] == 1 else partie_dict['nomE2']
  return partie_dict

def recompiler_partie(connexion, idp):
  """
    Renvoie un tableau 2D correspondant à une partie normale
  """
  # grille_actions = init_grille(connexion, idp)
  # grille = grille_actions[0]
  # actions = grille_actions[1]
  # partie = recuperer_partie_simple(connexion, idp)
  # #rejouer toutes les actions
  # for a in actions:
  #   numa=a[0]
  #   texte=a[1]
  #   #on cherche un pattern "x,y"
  #   if ',' in texte:
  #     parties = texte.split(',')
  #     # Extraire les chiffres
  #     x = int(parties[0][-1])  # Dernier caractère avant la virgule
  #     y = int(parties[1][0])   # Premier caractère après la virgule

  #     # Déterminer quelle équipe (1 ou 2)
  #     equipe = 1 if (numa % 2 != 0) else 2
  #     grille[x][y] = equipe

  # partie['grille']=grille

  # return partie
