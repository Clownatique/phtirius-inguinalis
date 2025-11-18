# from .utils import insert_requete
# from .utils import select_requete
import psycopg
from .utils import select_query, other_query,get_instances,count_instances,get_table_like
from datetime import datetime

def noms_pris(connexion):
    query =  'SELECT nome FROM equipe'
    return select_query(connexion, query)

def liste_equipes(connexion):
    query =  'SELECT nome, couleure FROM equipe'
    return select_query(connexion, query)

def liste_morpion_une_equipe(connexion,nom,couleur):
    requete = '''SELECT image,pv,atk,mana,reu from morpion m join
    posseder p using(idm) where p.nomE = %s and p.couleurE = %s'''
    params = [nom, couleur]
    return select_query(connexion, requete, params)

def couleur_prises(connexion):
    requete = 'SELECT couleure FROM equipe'
    return select_query(connexion, requete)

def liste_morpion(connexion):
    requete = "SELECT idm, image,pv,atk,mana,reu from morpion"
    return select_query(connexion, requete)

def insertion_equipe(connexion, nom, couleur):
    query = f"""INSERT INTO equipe (nome, couleure, date_creation) VALUES(%s,%s,%s)"""
    print(couleur)
    return other_query(connexion, query, [nom, couleur, datetime.now()])

def insertion_posseder(connexion, nom, couleur, liste_morpion):
    """
    Prends un tableau d'indice de morpion

    Renvoie
    """
    for indice_morpion in liste_morpion:
        # faire le traitement pour récupérer les stats
        # de base du morpion pour les affecter
        query = "SELECT pv, atk, mana, reu from morpion where idm = %s"
        stat = select_query(connexion, query, [int(indice_morpion)])[0]
        query ="INSERT INTO posseder values (%s,%s,%s,%s,%s,%s,%s)"
        print(nom)
        other_query(connexion, query,[indice_morpion,nom[0],couleur[0],stat[0],stat[1],stat[2],stat[3]])
