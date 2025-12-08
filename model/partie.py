from model import equipe
from .utils import other_query, select_query

def terminer_partie(connexion, idp,gagnant):
    query = """UPDATE Partie SET est_terminee = TRUE, date_fin = NOW(),
nomE_gagnant = %s WHERE idP = %s"""
    other_query(connexion, query, [gagnant, idp])
    # Ajouter une entrée dans le journal
    query_journal ="""
INSERT INTO Journal (numa, idP, texte_action, date_action, type_action)SELECT
COALESCE(MAX(numa), 0) + 1, %s, %s, NOW(), 'victoire'FROM Journal WHERE idP = %s """
    texte = f"Victoire de {gagnant}" if gagnant != 'egalite' else "Égalité"
    other_query(connexion, query_journal, [idp, texte, idp])

def verifier_gagne_elimination(morpions:list):
  return len(morpions) == 0 or len(morpions) == 0

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
      action=action+'+'
    else:
      action=action+'-'

def inserer_action(connexion, idp, action):
  """
  Insère une action dans le journal
  action = texte de l'action
  """
  #récupère le prochain numéro d'action
  requete_numa = "SELECT max(numa) FROM Journal WHERE idp = %s"
  numa = select_query(connexion,requete_numa,[idp])[0][0]
  if numa is None:
    numa = 1
  else:
    numa = int(numa)+1

  requete = """INSERT INTO JOURNAL (numa, idP, texte_action,date_action) VALUES (%s,%s,%s,NOW())"""
  valeurs = [numa, idp,action]
  return other_query(connexion, requete, valeurs)


def creer_partie(connexion, nomE1, nomE2, est_special,max_tours,taille_grille):
    sql = """INSERT INTO PARTIE (nomE1, nomE2, date_debut, est_speciale,max_tours,taille_grille)
          VALUES (%s, %s, NOW(), %s, %s, %s)"""

    valeurs=[nomE1, nomE2, est_special,max_tours,taille_grille]
    idp = other_query(connexion, sql, valeurs)
    return idp


def init_grille(connexion, idp) -> tuple:
  sel_partie="""WHERE idP = %s"""
  query = f"""SELECT numA, texte_action FROM journal {sel_partie} ORDER BY numA ASC"""
  actions = select_query(connexion,query, [idp])

  #récupère la taille de la grille :
  query_taille = """SELECT taille_grille FROM partie """+sel_partie
  info_partie = select_query(connexion, query_taille,[idp])
  taille_grille = info_partie[0][0] if info_partie else 3

  #initialisation de la grille vide
  grille = [[None for _ in range(taille_grille)] for _ in range(taille_grille)]
  return (grille,actions)


def recompiler_partie(connexion, idp):
  """
    Renvoie un tableau 2D correspondant à une partie normale
  """
  grille_actions = init_grille(connexion, idp)
  grille = grille_actions[0]
  actions = grille_actions[1]
  partie = recuperer_partie(connexion, idp)
  #rejouer toutes les actions
  for a in actions:
    numa=a[0]
    texte=a[1]
    #on cherche un pattern "x,y"
    if ',' in texte:
      parties = texte.split(',')
      # Extraire les chiffres
      x = int(parties[0][-1])  # Dernier caractère avant la virgule
      y = int(parties[1][0])   # Premier caractère après la virgule

      # Déterminer quelle équipe (1 ou 2)
      equipe = 1 if (numa % 2 != 0) else 2
      grille[x][y] = equipe

  partie['grille']=grille

  return partie

def recompiler_partie_avancee(connexion, idp):
  """
    Renvoie une grille 2D avec les morpions et leurs stats pour une partie avancée
    Recompile l'état en rejouant toutes les actions du journal
  """
  #récupère la taille de la grille et les équipes
  partie = recuperer_partie(connexion,idp)
  nomE1 = partie['nomE1']
  nomE2 = partie['nomE2']
  nomEs = [nomE1, nomE2]
  # récupère la grille et les actions (pas propre)
  grille_actions = init_grille(connexion, idp)
  grille = grille_actions[0]
  actions = grille_actions[1]
  lenactions = len(actions)
  if lenactions% 2 == 0 or lenactions == 0:
    numtour = 1
  else:
    numtour = 2
  partie['joueur'] = numtour
  #récupère tous les morpions initiales pour chaque équipe
  morpions = [
    recuperer_morpions_joueur(connexion,idp,i) for i in [nomE1, nomE2]
  ] # liste de deux dictionnaires
  #récupère toutes les actions du journal
  for action in actions:
    coup = action[1]
    num = action[0]
    indice = 0 if num % 2 == 1 else 0
    morpions_du_joueur= morpions[indice]
    if coup[0].isalpha():
      #ici, les sorts
      if coup[1:] == '-':
          # si le sort a échoué, alors on s'embête pas
          pass
      else:
        action = coup
        sort = coup[:2]
        acteur = grille[int(action[3])][int(action[5])]
        cible = grille[int(action[7])][int(action[9])]

        if sort == "at":
           cible['PV'] =- acteur['ATK']
        elif sort == "bf":
          cible['PV'] =-3
          cible['MANA'] =-2
        elif sort == 'sn':
          cible['PV'] =+1
          cible['MANA'] =1
        elif sort == 'ag':
          cible = None
          # à revoir pcq c pas comme ça qu'on détruit une case proprement
          acteur['MANA'] =-5
        if cible['PV'] < 0:
          cible = None

        # et on mets à jour la grille
        grille[int(action[3])][int(action[5])] = acteur
        grille[int(action[7])][int(action[9])] = cible

    else:
      # placement classique
      print(coup)
      id_morpion_a_placer = coup[4:]
      print(morpions_du_joueur)
      morpion = morpions_du_joueur[id_morpion_a_placer]
      grille[int(coup[0])][int(coup[2])] = morpion

  morpions_derniers = morpions[int(partie['joueur']-1)]
  partie['grille'] = grille
  partie['morpions'] = morpions_derniers
  return partie

def recuperer_morpions_joueur(connexion, idp, nom_equipe):
  """
  Récupère les morpions disponibles pour une équipe dans une partie
  """
  query = """SELECT m.idM, m.nomM, m.image, m.PV, m.ATK, m.MANA, m.REU,p.nomE
        FROM Morpion m JOIN Posseder p ON p.idM = m.idM
        WHERE p.nomE=%s"""
  morpions = select_query(connexion, query, [nom_equipe])
  morpions_dic_quipe = {
            str(m[0]): {
                'id':m[0],
                'image': m[2],
                'PV': m[3],
                'ATK': m[4],
                'MANA': m[5],
                'REU': m[6],
                'nomE':m[7]
            }
            for m in morpions
    }

  return morpions_dic_quipe

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
