from utils import insert_requete
from utils import select_requete

def liste_morpion(connexion) -> dict:
    with connexion.cursor() as cursor:
        try:
            cursor.execute("SELECT image,pv,atk,mana,reu from morpion")
            result = cursor.fetchall()
            REQUEST_VARS['liste_morpion'] = result
        except psycopg.Error as e:
            print(f"Error : {e}")

def insertion_equipe(connexion) -> dict:
    ""
    "" #on suppose ici que tout est bon 
    ""
    with connexion.cursor() as cursor:
        try:
            cursor.execute(f"""INSERT INTO equipe values ({POST["nom"]},{POST[]},{})""") 
            # évidemment grosse faille spatio temporelle de l'espace j'ai
            # jamais vu ça
        except psycopg.Error as e:
            print(f"Error : {e}")

def insertion_posseder(connexion, equipe_dict) -> int:
    with connexion.cursor() as cursor:
        try:
            cursor.execute(f"""INSERT INTO posseder values ({POST["nom"]},{POST[]},{})""") 
            # évidemment grosse faille spatio temporelle de l'espace j'ai
            # jamais vu ça
        except psycopg.Error as e:
            print(f"Error : {e}")



