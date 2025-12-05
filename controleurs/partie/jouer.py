from model.partie import inserer_action, recuperer_partie, terminer_partie
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
            REQUEST_VARS['erreur_action']="❌ Case hors limites"
            return False

        #verifie que la case est vide (0=vide)
        if grille[x][y]!=0:
            REQUEST_VARS['erreur_action']="❌ Case déjà occupée"
            return False 
        return True
    except Exception as e:
        print(f"Erreur vérification action : {e}")
        REQUEST_VARS['erreur_action']="❌ Action invalide"
        return False

def gagne_par_placement_equipe(grille, taille, verif_cellule):
    #verification des lignes
    for ligne in grille:
        if all(verif_cellule(cell) for cell in ligne):
            return True

    #vérification des colonnes
    for j in range(taille):
        if all(verif_cellule(grille[i][j]) for i in range(taille)):
            return True
    #verification des diagonales
    if all(verif_cellule(grille[i][i]) for i in range(taille)):
        return True
    if all(verif_cellule(grille[i][taille - 1 - i]) for i in range(taille)):
        return True

    return False

def verification_victoire_normale(grille, taille, equipe_joueuse):
    """
    Vérifie si l'équipe_joueuse a gagné (partie normale).
    """
    # Définition de la fonction de vérification pour l'équipe qui vient de jouer
    verif_cellule_joueuse = lambda cell: cell == equipe_joueuse

    # Vérification du placement UNIQUEMENT pour l'équipe joueuse
    if gagne_par_placement_equipe(grille, taille, verif_cellule_joueuse):
        return equipe_joueuse # Renvoie 1 ou 2

    # Verifier si grille pleine
    cases_libres = sum(
        1 for i in range(taille) for j in range(taille) if grille[i][j] == 0
    )
    if cases_libres == 0:
        return 'egalite'

    return None

# Note: L'appel à select_query nécessite l'objet connexion
def verifier_victoire_avancee(connexion, partie, grille):
    """
    Vérifie si une équipe a gagné (partie avancée).
    """
    # --- 1. Victoire par Élimination (Doit toujours être vérifié pour les deux équipes) ---
    taille=partie['taille']
    vivants_e1 = 0
    vivants_e2 = 0
    for i in range(taille):
        for j in range(taille):
            cell = grille[i][j]
            if cell and cell.get('morpion') and cell['morpion']['est_vivant']:
                morpion_equipe = cell['morpion']['equipe']
                if morpion_equipe == partie['nomE1']:
                    vivants_e1 += 1
                elif morpion_equipe == partie['nomE2']:
                    vivants_e2 += 1

    if vivants_e1 == 0 and vivants_e2 > 0:
        return partie['nomE2']
    if vivants_e2 == 0 and vivants_e1 > 0:
        return partie['nomE1']

    # --- 2. Victoire par Placement (UNIQUEMENT pour l'équipe joueuse) ---

    # Définition de la fonction de vérification de cellule pour l'équipe joueuse
    def verif_cellule_joueuse(cell):
        return (cell and cell.get('morpion') and
                cell['morpion']['equipe'] == nom_equipe_joueuse and
                cell['morpion']['est_vivant'])

    if gagne_par_placement_equipe(grille, taille, verif_cellule_joueuse):
        return nom_equipe_joueuse

    # --- 3. Vérifier si max tours atteint ---

    # ... (Le code de vérification max_tours reste inchangé) ...
    try:
        query_tours = "SELECT COUNT(*) FROM Journal WHERE idp = %s"
        nb_tours = select_query(connexion, query_tours, [partie['idP']])[0][0]
        if nb_tours >= partie['max_tours']:
            return 'egalite'
    except Exception as e:
        print(f"Erreur verification max tours: {e}")
    return None
    

erreur_bool = not REQUEST_VARS.get('url_components')
erreur_bool = erreur_bool or(REQUEST_VARS['url_components'][1] == '')
erreur_bool = erreur_bool or recuperer_partie(connexion, REQUEST_VARS['url_components'][1]) == None
if erreur_bool:
    REQUEST_VARS['erreur'] = "erreur"
else:
# donnée à fournir QUOI QU'IL EN SOIT
    idp = REQUEST_VARS['url_components'][1]
    partie = recuperer_partie(connexion,idp)

    tour = partie['tour']
    equipe_courrante = 'nomE1' if tour == 1 else 'nomE2'
    equipe_numero=1 if tour==1 else 2
    REQUEST_VARS['partie'] = partie
    REQUEST_VARS['taille'] = partie['taille']
    REQUEST_VARS['avancee'] = partie['est_speciale']
    REQUEST_VARS['max_tours'] = partie['max_tours']
    REQUEST_VARS['joueur']=partie[equipe_courrante]
    #chargement de la grille
    if partie['est_speciale']:
        grille=recompiler_partie_avancee(connexion, idp)
        REQUEST_VARS['grille_avancee']=grille
        var=recuperer_morpions_joueur(connexion, idp, REQUEST_VARS['joueur'])
        REQUEST_VARS['morpions'] = var
    else :
        grille=recompiler_partie(connexion,idp)
        REQUEST_VARS['grille']=grille

    #traitement de l'action
    if POST != {}:
    #il y'a toujours un champ case dans le post.
        if 'case' in POST:
            pos = POST['case'][0]
            # faire une bête vérif côté serveur pour éviter que le F mette des valeurs de cases bizzare...:w

            #PARTIE SPECIALE
            if partie['est_speciale']:
                if 'morpion_choisi' in POST:
                    #crée le texte d'action
                    action =f"{pos}<-{POST['morpion_choisi'][0]}"
                    print(f"Action avancée : {action}")

                    inserer_action(connexion,idp,action) #réutiliser ce qui marche déjà

                    #recharger la grille
                    grille=recompiler_partie_avancee(connexion,idp)
                    REQUEST_VARS['grille_avancee']=grille

                    #verifier victoire
                    gagnant = verifier_victoire_avancee(connexion,partie,grille)
                    if gagnant:
                        terminer_partie(connexion, idp, gagnant)
                        REQUEST_VARS['partie_terminee']=True
                    
                        if gagnant == 'egalite':
                            REQUEST_VARS['message_victoire']="Egalité !"
                        else:
                            REQUEST_VARS['message_victoire']=f"Victoire de {gagnant} !"
                    else :
                        REQUEST_VARS['message_succes']="✅ Action effectuée !"
                        
                        #recharger la partie pour mettre à jour le tour
                        partie=recuperer_partie(connexion, idp)
                        REQUEST_VARS['partie']=partie
                        tour=partie['tour']
                        equipe_courrante='nomE1' if tour==1 else 'nomE2'
                        REQUEST_VARS['joueur']=partie[equipe_courrante]
                else:
                    REQUEST_VARS['erreur_action']="❌ Veuillez sélectionner un morpion"

            # PARTIE NORMALE
            else :
                if verifier_action_simple(grille, pos):
                    inserer_action(connexion, idp, pos)

                    #recharger la grille
                    grille=recompiler_partie(connexion, idp)
                    REQUEST_VARS['grille']=grille

                    #verifier victoire
                    gagnant=verification_victoire_normale(grille,partie['taille'], equipe_numero)

                    if gagnant:
                        #convertir 1/2 en nom d'équipe
                        if gagnant==1:
                            nom_gagnant=partie['nomE1']
                        elif gagnant==2:
                            nom_gagnant=partie['nomE2']
                        else:
                            nom_gagnant='egalite'
                    
                        terminer_partie(connexion, idp, nom_gagnant)
                        REQUEST_VARS['partie_terminee']=True
                        
                        if nom_gagnant=='egalite':
                            REQUEST_VARS['message_victoire']="Egalite !"
                        else :
                            REQUEST_VARS['message_victoire']=f"Victoire de {nom_gagnant} !"
                    else:
                        REQUEST_VARS['message_succes']="✅ Morpion placé !"
                        #recharger la partie pour mettre à jour le tour
                        partie=recuperer_partie(connexion, idp)
                        REQUEST_VARS['partie']=partie
                        tour=partie['tour']
                        equipe_courrante='nomE1' if tour==1 else 'nomE2'
                        REQUEST_VARS['joueur']=partie[equipe_courrante]
        else:
            REQUEST_VARS['erreur_action']="❌ Aucune case sélectionnée"

"""
                if 'sort' in POST:
                    if POST['sort'] == 'bf':
                        None
                        # action = f"bf{}->{}"
                    elif POST['sort'] == 'at':
                        None
                    elif POST['sort'] == 'sn':
                        None
                    elif POST['sort'] == 'ag':
                        None
                        # action = f"ag:{}-"
                    else:
                        REQUEST_VARS['erreur_sort']"""
                
    
           
        
