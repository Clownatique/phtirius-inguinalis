import psycopg
from model.utils import select_query, other_query,get_instances,count_instances,get_table_like
from datetime import datetime

def noms_utilises(connexion):
    query =  'SELECT nome FROM equipe'
    return select_query(connexion, query)

def liste_equipes(connexion):
    query =  'SELECT nome, couleure FROM equipe'
    return select_query(connexion, query)

def liste_morpion_une_equipe(connexion,nom):
    requete = '''SELECT image,m.pv,m.atk,m.mana,m.reu from morpion m join
    posseder p using(idm) where p.nomE = %s '''
    params = [nom]
    return select_query(connexion, requete, params)

def couleur_prises(connexion):
    requete = 'SELECT couleure FROM equipe'
    return select_query(connexion, requete)

def liste_morpion(connexion):
    requete = "SELECT idm, image,pv,atk,mana,reu from morpion"
    return select_query(connexion, requete)

def insertion_equipe(connexion, nom, couleur):
    query = f"""INSERT INTO equipe (nome, couleure, date_creation) VALUES(%s,%s,%s)"""
    return other_query(connexion, query, [nom[0], couleur[0], datetime.now()])

def insertion_posseder(connexion, nom, couleur, liste_morpion):
    """
    Prends un tableau d'indice de morpion
    Renvoie le nombre de morpions insérés
    """
    for indice_morpion in liste_morpion:
        # faire le traitement pour récupérer les stats
        # de base du morpion pour les affecter
        query ="INSERT INTO posseder values (%s,%s)"
        other_query(connexion, query,[int(indice_morpion), nom[0]])

def supprimer_equipe(connexion, nom):
    query = f"""DELETE FROM Equipe WHERE nome = %s"""
    other_query(connexion,query, [nom])
