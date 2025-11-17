import time

def creer_partie(idEquipe1, idEquipe2):
  connexion=
  cur=connexion.cursor()
  sql = """INSERT INTO PARTIE (idEquipe1, idEquipe2, date_debut) 
          VALUES (%s, %s, %s) 
          RETURNING idPartie;"""
  valeurs=(idEquipe1, idEquipe2, datetime.now())
  cur.execute(sql,valeurs)
           
  
