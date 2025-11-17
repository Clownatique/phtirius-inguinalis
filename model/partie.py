from datetime import datetime

def creer_partie(connexion, idEquipe1, idEquipe2):
  try :
    cur=connexion.cursor()
    sql = """INSERT INTO PARTIE (idEquipe1, idEquipe2, date_debut) 
          VALUES (%s, %s, %s) 
          RETURNING idPartie;"""
    valeurs=(idEquipe1, idEquipe2, datetime.now())
    cur.execute(sql,valeurs)
    cur.fetchone()

   
    
           
  
