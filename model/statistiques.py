from model.utils import select_query

def compter_instances(connexion):
    """
    compte le nombre d'instances dans 3 tables
    renvoie un dictionnaire avec les comptes
    """
    stats={}
    try:
        #nombre d'équipes
        query_equipes="SELECT COUNT(*) FROM Equipe"
        stats['equipes']=select_query(connexion, query_equipes)[0][0]

        #nombre de morpions
        query_morpions="SELECT COUNT(*) FROM Morpion"
        stats['morpions']=select_query(connexion, query_morpions)[0][0]

        #nombre de parties
        query_parties="SELECT COUNT(*) FROM Partie"
        stats['parties']=select_query(connexion, query_parties)[0][0]
    except Exception as e:
        print(f"Erreur compter_instances : {e}")
        stats={'equipes': 0, 'morpions': 0, 'parties' : 0}
    return stats

def top_3_equipes(connexion):
    """
    récupère le top 3 des équipes avec le plus de victoires
    renvoie un liste de tuples (nomE, nb_victoires, couleurE)
    """
    try:
        query="""
            SELECT e.nomE, COUNT(*) as victoires, e.couleurE
            FROM Partie p JOIN Equipe e ON p.nomE_gagnant=e.nomE
            WHERE p.nomE_gagnant IS NOT NULL
            GROUP BY e.nomE, e.couleurE
            ORDER BY victoires DESC
            LIMIT 3
            """
        return select_query(connexion, query)
    except Exception as e:
        print(f"Erreur top_3_equipes : {e}")
        return []

def parties_extremes(connexion):
    """
    recupère la partie la plus rapide et la plus longue
    renvoie un dictionnaire avec les infos des parties
    """
    stats={}
    try:
        #partie la plus rapide :
        #date_part('epoch', date_fin - date_debut) = durée en secondes entre 2 dates
        query_rapide="""
                    SELECT p.nomE1, p.nomE2, p.nomE_gagnant, DATE_PART('epoch', p.date_fin - p.date_debut) AS duree_secondes
                    FROM Partie p 
                    WHERE p.date_fin IS NOT NULL AND p.date_debut IS NOT NULL
                    ORDER BY duree_secondes ASC
                    LIMIT 1
                    """
        result_rapide=select_query(connexion, query_rapide)
        if result_rapide:
            stats['rapide']={
                    'nomE1': result_rapide[0][0],
                    'nomE2': result_rapide[0][1],
                    'gagnant' : result_rapide[0][2],
                    'duree' : int(result_rapide[0][3]) #en secondes
            }
        else :
            stats['rapide']=None
        
        #partie la plus longue :
        query_longue="""
                    SELECT p.nomE1, p.nomE2, p.nomE_gagnant, DATE_PART('epoch', p.date_fin - p.date_debut) AS duree_secondes
                    FROM Partie p
                    WHERE p.date_fin IS NOT NULL AND p.date_debut IS NOT NULL
                    ORDER BY duree_secondes DESC
                    LIMIT 1
                    """
        result_longue=select_query(connexion, query_longue)

        if result_longue:
            stats['longue']={
                'nomE1': result_longue[0][0],
                'nomE2': result_longue[0][1],
                'gagnant' : result_longue[0][2],
                'duree' : int(result_longue[0][3]) #en secondes
            }
        else:
            stats['longue']=None
        
    except Exception as e:
        print(f"Erreur parties_extremes : {e}")
        stats = {'rapide' : None, 'longue': None}
    return stats

def moyenne_journal_par_mois(connexion):
    """
    calcule le nombre moyen de lignes de journalisation par mois/année
    renvoie une liste de tuples (mois, annee, moyenne)
    """
    try:
        query="""
            SELECT
                EXTRACT(MONTH FROM date_action) as mois,
                EXTRACT(YEAR FROM date_action) as annee,
                COUNT(*) * 1.0 / COUNT(DISTINCT idp) as moyenne_actions
            FROM Journal
            GROUP BY mois, annee
            ORDER BY annee DESC, mois DESC
            LIMIT 12
            """
        return select_query(connexion, query)
    except Exception as e:
        print(f"Erreur moyenne_journal_par_mois : {e}")
        return []
    
def formater_duree(secondes):
    """
    convertit une durée en secondes en format lisible
    ex : 65 -> "1m 5s" ou 3661 -> "1h 1m 1s"
    """
    if secondes<60:
        return f"{secondes}s"
    elif secondes>3600:
        minutes=secondes//60
        secondes_rest=secondes%60
        return f"{minutes}m {secondes_rest}s"
    else :
        heures=secondes//3600
        minutes=(secondes%3600)//60
        secondes_rest=secondes%60
        return f"{heures}h {minutes}m {secondes_rest}s"
                

