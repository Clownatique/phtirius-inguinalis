import psycopg
from model.utils import select_query, other_query,get_instances,count_instances,get_table_like
from datetime import datetime

def noms_utilises(connexion):
    query =  'SELECT nomE FROM equipe'
    return select_query(connexion, query)

def liste_equipes(connexion):
    query =  'SELECT nomE, couleurE, date_creation FROM equipe'
    return select_query(connexion, query)

def liste_morpion_une_equipe(connexion,nom):
    requete = '''SELECT m.image, m.pv, m.atk, m.mana, m.reu from morpion m join
    posseder p using(idm) where p.nomE = %s '''
    params = [nom]
    return select_query(connexion, requete, params)

def couleur_prises(connexion):
    requete = 'SELECT couleurE FROM equipe'
    return select_query(connexion, requete)

def liste_morpion(connexion):
    requete = "SELECT idm, nomM, image,pv,atk,mana,reu from morpion"
    return select_query(connexion, requete)

def insertion_equipe(connexion, nom, couleur):
    try :
        query = f"""INSERT INTO equipe (nomE, couleurE, date_creation) VALUES(%s,%s,%s)"""
        return other_query(connexion, query, [nom, couleur, datetime.now()])
    except psycopg.IntegrityError :
        raise ValueError(f"Le nom '{nom}' ou la couleur '{couleur}' est déjà utilisé")

def insertion_posseder(connexion, nom, couleur, liste_morpion):
    """
    Prends un tableau d'indice de morpion
    Renvoie le nombre de morpions insérés
    """
    nb_inseres=0
    for indice_morpion in liste_morpion:
        # faire le traitement pour récupérer les stats
        # de base du morpion pour les affecter
        query ="INSERT INTO posseder (idM, nomE) values (%s,%s)"
        other_query(connexion, query,[int(indice_morpion), nom])
        nb_inseres+=1
    return nb_inseres

def supprimer_equipe(connexion, nom):
    query = """DELETE FROM Equipe WHERE nomE = %s"""
    return other_query(connexion,query, [nom])
