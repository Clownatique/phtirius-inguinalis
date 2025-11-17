# from .utils import insert_requete
# from .utils import select_requete
import psycopg
from .utils import select_query, other_query,get_instance,count_instances,get_table_like
from datetime import now


def noms_pris(connexion) -> list:
    query =  'SELECT nome FROM equipe'
    return select_query(connexion, query)

def liste_equipes(connexion) -> dict:
    query =  'SELECT nome, couleure FROM equipe'
    return select_query(connexion, query)

def liste_morpion_une_equipe(connexion,nom,couleur):
    requete = 'SELECT image,pv,atk,mana,reu from morpion m join
    posseder p using(idm) where p.nomE = %s and p.couleurE = %s'
    params = [nom, couleur]
    return select_query(connexion, requete, params)

def couleur_prises(connexion) -> list:
    requete = 'SELECT couleure FROM equipe'
    return select_query(connexion, requete)

def liste_morpion(connexion) -> list:
    requete = "SELECT image,pv,atk,mana,reu from morpion"
    return select_query(connexion, requete)

def insertion_equipe(connexion, nom, couleur) -> int:
    query = f"""INSERT INTO equipe nome, couleure, date, values(%s,%s,{now()})"""
    return execute_other_query(connexion, query, [nom, couleur])

def insertion_posseder(connexion, nom, couleur, liste_morpion) -> int:
    """
    Prends un tableau d'indice de morpion

    Renvoie
    """
    instance_affecte = 0
    for indice_morpion in liste_morpion:
        # faire le traitement pour récupérer les stats
        # de base du morpion pour les affecter
        query ="INSERT INTO posseder values (%s,%s,%s,)"
        instance_affecte =+ other_query(query,[nom,couleur, indice_morpion])
    return instance_affecte

