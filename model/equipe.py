# from .utils import insert_requete
# from .utils import select_requete
import psycopg

def noms_pris() -> list:
    with connexion.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM equipe')
            result = cursor.fetchall()
            return result
        except psycopg.Error as e:
            return e


def liste_equipes(connexion) -> dict:
    with connexion.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM equipe')
            result = cursor.fetchall()
            return result
        except psycopg.Error as e:
            return e

def liste_morpion_une_equipe(connexion,nom,couleur):
    with connexion.cursor() as cursor:
        try:
            requete = f'''SELECT image,pv,atk,mana,reu from morpion m join
            posseder p using(idm) where p.nomE = '{nom}' and p.couleurE
            = '{couleur}' '''
            print(requete)
            cursor.execute(requete)
            return cursor.fetchall()
        except psycopg.Error as e:
            return e

def couleur_prises(connexion, couleur:str) -> bool:
     with connexion.cursor() as cursor:
        try:
            requete = f'''SELECT couleur FROM equipe'''
            print(requete)
            result = cursor.execute(requete)
            return result
        except psycopg.Error as e:
            return e

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
            cursor.execute(f"""INSERT INTO equipe values({POST["nom"]},{POST["couleur"]})""") 
            # évidemment grosse faille spatio temporelle de l'espace j'ai
            # jamais vu ça
        except psycopg.Error as e:
            print(f"Error : {e}")

def insertion_posseder(connexion, equipe_dict) -> int:
    with connexion.cursor() as cursor:
        try:
            cursor.execute(f"""INSERT INTO posseder values
                           ({POST["nom"]},{POST["couleur"]},{POST["idM"]})""") 
            # évidemment grosse faille spatio temporelle de l'espace j'ai
            # jamais vu ça
        except psycopg.Error as e:
            print(f"Error : {e}")



