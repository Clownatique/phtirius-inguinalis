from model.partie import inserer_action, recuperer_partie
from model.partie_flora import recompiler_partie, recompiler_partie_avancee, recuperer_morpions_joueur
from model.utils import select_query, other_query

connexion = SESSION['CONNEXION']

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

def verification_victoire_normale(grille, taille):
    """
    Vérifie si une équipe a gagné (partie normale)
    renvoie : 
        - 1 si equipe 1 gagne
        - 2 si equipe 2 gagne
        - 'egalite' si grille pleine sans gagnant
        - None si partie en cours
    """
    #on verifie les lignes
    for i in range(taille):
        if all(grille[i][j] == 1 for j in range(taille)):
            return 1
        if all(grille[i][j]==2 for j in range(taille)):
            return 2
    #on vérifie les colonnes
    for j in range(taille):
        if all(grille[i][j] == 1 for i in range(taille)):
            return 1
        if all(grille[i][j]==2 for i in range(taille)):
            return 2

    #verification diagonale (haut-gauche à bas-droit)
    if all(grille[i][i]==1 for i in range(taille)):
        return 1
    if all(grille[i][i]==2 for i in range(taille)):
        return 2

    #verification diagonale (haut-droit à bas-gauche)
    if all(grille[i][taille-1-i]==1 for i in range(taille)):
        return 1
    if all(grille[i][taille-1-i] == 2 for i in range(taille)):
        return 2

    #verifier si grille pleine
    cases_libres=sum(1 for i in range(taille) for j in range(taille) if grille[i][j]==0)
    if cases_libres == 0:
        return 'egalite'
    
    return None

def verifier_victoire_avancee(grille, taille, partie):
    """
    Vérifie si une équipe a gagné (partie avancée)
    
    RENVOIE:
        - nomE1 ou nomE2 si victoire
        - 'egalite' si max tours atteint
        - None si partie en cours
    """
    # Compter les morpions vivants de chaque équipe
    vivants_e1 = 0
    vivants_e2 = 0
    
    for i in range(taille):
        for j in range(taille):
            if grille[i][j] and grille[i][j].get('morpion'):
                morpion = grille[i][j]['morpion']
                if morpion['est_vivant']:
                    if morpion['equipe'] == partie['nomE1']:
                        vivants_e1 += 1
                    else:
                        vivants_e2 += 1
    
    # Victoire par élimination
    if vivants_e1 == 0 and vivants_e2 > 0:
        return partie['nomE2']
    if vivants_e2 == 0 and vivants_e1 > 0:
        return partie['nomE1']
    
    # Vérifier alignements (comme partie normale)
    # On vérifie si une équipe a aligné 'taille' morpions
    
    # Lignes
    for i in range(taille):
        ligne = [grille[i][j] for j in range(taille)]
        if all(cell and cell.get('morpion') and cell['morpion']['equipe'] == partie['nomE1'] and cell['morpion']['est_vivant'] for cell in ligne):
            return partie['nomE1']
        if all(cell and cell.get('morpion') and cell['morpion']['equipe'] == partie['nomE2'] and cell['morpion']['est_vivant'] for cell in ligne):
            return partie['nomE2']
    
    # Colonnes
    for j in range(taille):
        colonne = [grille[i][j] for i in range(taille)]
        if all(cell and cell.get('morpion') and cell['morpion']['equipe'] == partie['nomE1'] and cell['morpion']['est_vivant'] for cell in colonne):
            return partie['nomE1']
        if all(cell and cell.get('morpion') and cell['morpion']['equipe'] == partie['nomE2'] and cell['morpion']['est_vivant'] for cell in colonne):
            return partie['nomE2']
    
    # Diagonales
    diag1 = [grille[i][i] for i in range(taille)]
    if all(cell and cell.get('morpion') and cell['morpion']['equipe'] == partie['nomE1'] and cell['morpion']['est_vivant'] for cell in diag1):
        return partie['nomE1']
    if all(cell and cell.get('morpion') and cell['morpion']['equipe'] == partie['nomE2'] and cell['morpion']['est_vivant'] for cell in diag1):
        return partie['nomE2']
    
    diag2 = [grille[i][taille-1-i] for i in range(taille)]
    if all(cell and cell.get('morpion') and cell['morpion']['equipe'] == partie['nomE1'] and cell['morpion']['est_vivant'] for cell in diag2):
        return partie['nomE1']
    if all(cell and cell.get('morpion') and cell['morpion']['equipe'] == partie['nomE2'] and cell['morpion']['est_vivant'] for cell in diag2):
        return partie['nomE2']
    
    # Vérifier si max tours atteint
    # Récupérer le nombre de tours depuis le journal
    query_tours = "SELECT COUNT(*) FROM Journal WHERE idp = %s"
    nb_tours = select_query(connexion, query_tours, [partie['idP']])[0][0]
    
    if nb_tours >= partie['max_tours']:
        return 'egalite'
    
    return None

def terminer_partie(connexion, idP, gagnant):
    """
    Marque la partie comme terminée et enregistre le gagnant
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



if not REQUEST_VARS.get('url_components') or (len(REQUEST_VARS['url_components']) < 3) or (REQUEST_VARS['url_components'][2] == ''):
    # on vérifie l'url
    REQUEST_VARS['erreur'] = "erreur"
else:
    idp = REQUEST_VARS['url_components'][1]

    #récupération de la partie 

    partie = recuperer_partie(connexion,idp)
    if partie is None :
        #partie introuvable
        REQUEST_VARS['erreur']="erreur"
    else:
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

        #chargement de la grille
        if partie['est_speciale']:
            grille=recompiler_partie_avancee(connexion, idp)
            REQUEST_VARS['grille_avancee']=grille

            #charger les morpions du joueur actif
            REQUEST_VARS['morpions_joueur']=recuperer_morpions_joueur(connexion, idp, REQUEST_VARS['joueur'])
        else:
            grille=recompiler_partie(connexion, idp)
            REQUEST_VARS['grille']=grille

    #chargement initial de la grille (avant action)


        if partie['est_speciale']:
            grille=recompiler_partie_avancee(connexion, idp)
            REQUEST_VARS['grille_avancee']=grille
            REQUEST_VARS['morpions_joueur']=recuperer_morpions_joueur(connexion, idp, REQUEST_VARS['joueur'])
        else:
            grille=recompiler_partie(connexion,idp)
            REQUEST_VARS['grille']=grille

    #traitement de l'action jouée par le joueur
        if POST != {}:
            if 'case' in POST:
                case=POST['case'][0] #format : "x,y"
                print(f"Action reçue : {case}")

            #verifier si l'action est valide
                if verifier_action_simple(grille, case):
                    inserer_action(connexion,partie['idP'],case)

                #recharger la partie et la grille
                    partie = recuperer_partie(connexion, idp)
                    REQUEST_VARS['partie']=partie

                    if partie['est_speciale']:
                        grille=recompiler_partie_avancee(connexion, idp)
                        REQUEST_VARS['grille_avancee']=grille
                        REQUEST_VARS['morpiond_joueur']=recuperer_morpions_joueur(connexion, idp, REQUEST_VARS['joueur'])
                    else :
                        grille=recompiler_partie(connexion,idp)
                        REQUEST_VARS['grille']=grille

                #mettre à jour le joueur actif
                    tour = partie['tour']
                    if tour == 1:
                        REQUEST_VARS['joueur']=partie['nomE1']
                    else:
                        REQUEST_VARS['joueur']=partie['nomE2']

                    REQUEST_VARS['message_succes']="✅ Action effectuée avec succès !"

                else:
                #action invalide
                    REQUEST_VARS['erreur_action']="❌ Case déjà occupée ou action invalide"
            else :
                REQUEST_VARS['erreur_action']="❌ Aucune case sélectionnée"

                

