from model.partie import inserer_action, recuperer_partie, terminer_partie
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

def verifier_pos(pos, grille):
    if grille[int(pos[0])][int(pos[1])] != None:
        return False
        REQUEST_VARS['erreur_action']="❌ Case déjà occupée"
    return True

def verifier_action_complexe(grille, action):
    return True

def gagne_par_placement_equipe(grille, taille, verif_cellule):
    for ligne in grille:
        if all(verif_cellule(cell) for cell in ligne):
            return True
    colonnes_transposes = zip(*grille)
    for colonne in colonnes_transposes:
        if all(verif_cellule(cell) for cell in colonne):
            return True
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
    return None
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
    except (NameError, IndexError):
        nb_tours = 0
        # print("Avertissement: select_query ou connexion non défini. Impossible de vérifier max_tours.")
    if nb_tours >= partie['max_tours']:
        return 'egalite'

    return None

erreur_bool = not REQUEST_VARS.get('url_components')
erreur_bool = erreur_bool or(REQUEST_VARS['url_components'][0] == '')
erreur_bool = erreur_bool or recuperer_partie(connexion, REQUEST_VARS['url_components'][1]) == None
if erreur_bool:
    REQUEST_VARS['erreur'] = "erreur"
else:
# donnée à fournir QUOI QU'IL EN SOIT
    idp = REQUEST_VARS['url_components'][1]
    partie = recuperer_partie(connexion,idp)

    tour = partie['tour']
    equipe_courrante = 'nomE1' if tour == 1 else 'nomE2'
    REQUEST_VARS['taille'] = 3
    REQUEST_VARS['partie'] = partie
    REQUEST_VARS['avancee'] = partie['est_speciale']
    REQUEST_VARS['taille'] = partie['taille']
    REQUEST_VARS['max_tours'] = partie['max_tours']
    REQUEST_VARS['joueur']=partie[equipe_courrante]
    if partie['est_speciale']:
        grille=recompiler_partie_avancee(connexion, idp)
        var=recuperer_morpions_joueur(connexion, idp, REQUEST_VARS['joueur'])
        REQUEST_VARS['morpions'] = var
    else :
        grille=recompiler_partie(connexion,idp)
    REQUEST_VARS['grille']=grille
    if POST != {}:
    #il y'a toujours un champ case dans le post.
        if 'case' in POST:
            pos = POST['case'][0].split(',')
            # faire une bête vérif côté serveur pour éviter que le F mette des valeurs de cases bizzare...:w
            verifier_pos(pos,grille)

            if partie['est_speciale']:
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
                        REQUEST_VARS['erreur_sort']
                if 'morpion_choisi' in POST:
                    action =f'''{POST['case'][0]}<-{POST['morpion_choisi'][0]}'''
                    print(action)
                    inserer_action(connexion,idp,action) #réutiliser ce qui marche déjà
                    if verifier_victoire_avancee(connexion,partie,grille):
                        None
                else:
                    REQUEST_VARS['erreur_action'] = "pas de morpion"

            else:
                action = POST['case'][0]
                inserer_action(connexion,idp,action)
        else:
            REQUEST_VARS['erreur_action']="❌ Aucune case sélectionnée"
