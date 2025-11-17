from psycopg import sql

def get_liste_equipes(connexion):
  try :
    cur = connexion.cursor()
  
    #on récupère le nom de l'équipe, sa couleur et sa date de création (trié par nom alphabétique ?) :
    cur.execute("""
              SELECT nomE, couleurE, date_creation
              FROM Equipe
              ORDER BY nomE; 
              """) 
  
    equipes_data = cur.fetchall(); #récupère les résultat sous forme d'une liste de tuples
    liste_equipes = []


  #on parcours toutes les équipes
    for equipe in equipes_data : 
      nom = equipe[0]
      couleur = equipe[1]
      date_crea = equipe[2]
    
    #on récupère tous les morpions pour cette équipe
      cur.execute("""
                  SELECT m.nomM
                  FROM Posseder p JOIN Morpion m ON p.idM=m.idM
                  WHERE p.nomE = %s AND p.couleurE = %s
                  ORDER BY m.nomM;
                  """, (nom, couleur))
      result = cur.fetchall()

      morpions = [] # Créer une liste vide pour stocker les noms des morpions
      for ligne in result : 
        morpions.append(ligne[0])  # ligne[0] contient le nom du morpion
    # Créer un dictionnaire pour l'équipe
      equipe_dict = {}
      equipe_dict["info"] = "Equipe : " + nom + " - Couleur : " + couleur + " - Créée le " + str(date_crea)
      equipe_dict["morpions"] = morpions
      liste_equipes.append(equipe_dict)

    return liste_equipes
  except psycopg.Error as e:
    return e
    
  




