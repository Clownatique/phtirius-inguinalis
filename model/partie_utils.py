from .utils import select_query, other_query

def terminer_partie(connexion, idp, gagnant):
    query = """UPDATE Partie SET est_terminee = TRUE, date_fin = NOW(),
nomE_gagnant = %s WHERE idP = %s"""
    other_query(connexion, query, [gagnant, idp])
    # Ajouter une entrée dans le journal
    query_journal ="""
INSERT INTO Journal (numa, idP, texte_action, date_action, type_action)SELECT
COALESCE(MAX(numa), 0) + 1, %s, %s, NOW(), 'victoire'FROM Journal WHERE idP = %s """
    texte = f"Victoire de {gagnant}" if gagnant != 'egalite' else "Égalité"
    other_query(connexion, query_journal, [idp, texte, idp])


def verifier_gagne_pos(grille:list):
    # Dimensions de la grille
    lignes = len(grille)
    colonnes = len(grille[0])
    # Vérification des lignes horizontales
    def verifier_ligne_horizontale():
        for ligne in grille:
            if all(ligne):  # Tous True dans la ligne
                return True
        return False

    # Vérification des colonnes verticales
    def verifier_colonne_verticale():
        for col in range(colonnes):
            if all(grille[ligne][col] for ligne in range(lignes)):
                return True
        return False

    # Vérification des diagonales
    def verifier_diagonales():
        # Diagonale principale (de gauche à droite)
        if all(grille[i][i] for i in range(min(lignes, colonnes))):
            return True

        # Diagonale secondaire (de droite à gauche)
        if all(grille[i][colonnes-1-i] for i in range(min(lignes, colonnes))):
            return True

        return False

    # Combinaison de toutes les vérifications
    return (
        verifier_ligne_horizontale() or
        verifier_colonne_verticale() or
        verifier_diagonales()
    )

def init_grille(connexion, idp) -> tuple:
  query_taille = """SELECT taille_grille FROM partie WHERE idP = %s"""
  info_partie = select_query(connexion, query_taille,[idp])
  taille_grille = info_partie[0][0] if info_partie else 3 # par défault grille=3
  #initialisation de la grille vide
  grille = [[None for _ in range(taille_grille)] for _ in range(taille_grille)]
  return grille


def inserer_action(connexion, idp, action):
  """
  Insère une action dans le journal
  action = texte de l'action
"""
  # récupère le prochain numéro d'action
  requete_numa = "SELECT max(numa) FROM Journal WHERE idP = %s"
  res = select_query(connexion, requete_numa, [idp])
  numa = None
  if res and res[0]:
      numa = res[0][0]

  if numa is None:
      next_numa = 1
  else:
      next_numa = int(numa) + 1

  requete = """INSERT INTO JOURNAL (numa, idP, texte_action, date_action) VALUES (%s, %s, %s, NOW())"""
  valeurs = [next_numa, idp, action]
  return other_query(connexion, requete, valeurs)


def creer_partie(connexion, nomE1, nomE2, est_special,max_tours,taille_grille):
    sql = """INSERT INTO PARTIE (nomE1, nomE2, date_debut, est_speciale,max_tours,taille_grille)
          VALUES (%s, %s, NOW(), %s, %s, %s)"""

    valeurs=[nomE1, nomE2, est_special,max_tours,taille_grille]
    idp = other_query(connexion, sql, valeurs)
    return idp
