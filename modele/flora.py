from bdw import get_db_connector

def get_liste_equipes():
  connexion = get_db_connector()
  cur = connexion.cursor()
  
  #on récupère le nom de l'équipe, sa couleur et sa date de création (trié par nom alphabétique ?) :
  cur.execute("""
              SELECT nomE, couleurE, date_creation
              FROM Equipe
              ORDER BY nomE; 
              """) 
  
  equipes_data = cur.fetchall(); #données brutes des équipes
  liste_equipes = []
  for (nom, couleur, date_crea) in equipes_data : 
    #on récupère tous les morpions pour cette équipe
    cur.execute("""
                SELECT m.nomM
                FROM Posseder p JOIN Morpion m ON p.idM=m.idM
                WHERE p.nomE = %s AND p.couleurE = %s
                ORDER BY m.nomM;
                """, (nom, couleur))
    
    morpions = [ligne[0] for ligne in cur.fetchall()]
    liste_equipes.append({"info": f"Equipe : {nom} - Couleur : {couleur} - Créée le {date_crea}",
                          "morpions": morpions})
  return liste_equipes
    
  
