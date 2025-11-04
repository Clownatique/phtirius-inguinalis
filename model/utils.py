import psycopg

def requete_bete(connexion,requete:str):
    with connexion.cursor() as cursor:
        try:
            cursor.execute(requete)
            result = cursor.fetchall()
            return result
        except psycopg.Error as e:
            print(f"Error : {e}")
            return None
