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
