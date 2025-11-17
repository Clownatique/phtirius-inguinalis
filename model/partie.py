from datetime import datetime

def creer_partie(connexion, nomE1, couleurE1, nomE2, couleurE2):
  try :
    cur=connexion.cursor()
    sql = """INSERT INTO PARTIE (couleurE1, nomE1, couleurE2, nomE2, date_debut, est_special) 
          VALUES (%s, %s, %s, %s, %s, %s) 
          RETURNING idP;"""
    valeurs=(couleurE1, nomE1, couleurE2, nomE2, datetime.now(), est_special)
    cur.execute(sql,valeurs)
    idP=cur.fetchone()[0]
    connexion.close()
    cur.close()
    return idP
  except psycopg.Error as e:
    return e


    

   
    
           
  
