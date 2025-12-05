from model.partie import inserer_action, recuperer_partie
from model.partie_flora import recompiler_partie, recompiler_partie_avancee, recuperer_morpions_joueur
from model.utils import select_query, other_query

connexion = SESSION['CONNEXION']

#pyright: reportUndefinedVariable=false

def verifier_action_simple(grille, action):
    """
    verifie si une case est libre (partie normale)
    prends :
        - grille: tableau 2D
        - action : string "x,y"
    renvoie :
        - True si la case est libre, false sinon
    """
    try:
        pos = action.split(',')
        x=int(pos[0])
        y=int(pos[1])

        #vérifie que la case est dans les limites
        if x<0 or y<0 or x>=len(grille) or y>=len(grille[0]):
            return False

        #verifie que la case est vide (0=vide)
        return grille[x][y]==0
    except Exception as e:
        print(f"Erreur vérification action : {e}")
        return False

def terminer_partie(connexion, idP,gagnant):
    """"
    """
    if gagnant == 'egalite':
        query = """
            UPDATE Partie
            SET est_terminee = TRUE, date_fin = NOW()
            WHERE idP = %s
        """
        other_query(connexion, query, [idP])
    else:
        query = """
            UPDATE Partie
            SET est_terminee = TRUE, date_fin = NOW(), nomE_gagnant = %s
            WHERE idP = %s
        """
        other_query(connexion, query, [gagnant, idP])

    # Ajouter une entrée dans le journal
    query_journal = """
        INSERT INTO Journal (numa, idP, texte_action, date_action, type_action)
        SELECT COALESCE(MAX(numa), 0) + 1, %s, %s, NOW(), 'victoire'
        FROM Journal WHERE idP = %s
    """
    texte = f"Victoire de {gagnant}" if gagnant != 'egalite' else "Égalité - Maximum de tours atteint"
    other_query(connexion, query_journal, [idP, texte, idP])


if not REQUEST_VARS.get('url_components') or (REQUEST_VARS['url_components'][0] == '') or recuperer_partie(connexion, REQUEST_VARS['url_components'][1]) == None:
    REQUEST_VARS['erreur'] = "erreur"
else:
    if POST != {}:
    #il y'a toujours un champ case dans le post.
        if 'case' in POST:
            case=POST['case'][0] #format : "x,y"
            print(f"Action reçue : {case}")
        else:
            REQUEST_VARS['erreur_action']="❌ Aucune case sélectionnée"

        if

        REQUEST_VARS['erreur_action']="❌ Case déjà occupée ou action invalide"
    else:
    # donnée à fournir QUOI QU'IL EN SOIT
        idp = REQUEST_VARS['url_components'][1]
        if partie['est_speciale']:
            grille=recompiler_partie_avancee(connexion, idp)
            if verifier_action_complexe(action):
                None
            else:
                None
            REQUEST_VARS['morpiond_joueur']=recuperer_morpions_joueur(connexion, idp, REQUEST_VARS['joueur'])
            #verifier si l'action est valide
            #recharger la partie et la grille
        else :
            grille=recompiler_partie(connexion,idp)
            if verifier_action_simple(grille, case):
                inserer_action(connexion,partie['idP'],case)

        REQUEST_VARS['grille']=grille
            #mettre à jour le joueur actif
        tour = partie['tour']
        if tour == 1:
            REQUEST_VARS['joueur']=partie['nomE1']
        else:
            REQUEST_VARS['joueur']=partie['nomE2']

        idp = REQUEST_VARS['url_components'][1]
        REQUEST_VARS['taille'] = 3
        #récupération de la partie
        partie = recuperer_partie(connexion,idp)
        #partie trouvée
        REQUEST_VARS['partie'] = partie
        REQUEST_VARS['avancee'] = partie['est_speciale']
        REQUEST_VARS['taille'] = partie['taille']
        REQUEST_VARS['max_tours'] = partie['max_tours']

        #quelle équipe doit jouer ?
        tour = partie['tour']
        if tour==1:
            REQUEST_VARS['joueur']=partie['nomE1']
        else :
            REQUEST_VARS['joueur']=partie['nomE2']
            #chargement initial de la grille (avant action)
