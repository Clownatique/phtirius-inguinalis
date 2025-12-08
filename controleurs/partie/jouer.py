from model.partie import inserer_action, recuperer_partie, terminer_partie,recompiler_partie
import re
from model.partie import inserer_action, recuperer_partie, terminer_partie
from model.partie_flora import recompiler_partie, recompiler_partie_avancee, recuperer_morpions_joueur
from model.utils import select_query, other_query
import random

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

def verifier_adjacence(x1, y1, x2, y2):
    """
    vérifie si 2 cases sont adjacentes (horizontalement ou verticalement)
    renvoie true si oui sinon false
    """
    return (abs(x1-x2)==1 and y1==y2) or (abs(y1-y2)==1 and x1 == x2)

def calculer_reussite(reu_actuel):
    """
    calcule si une action réussit selon la proba et retourne true or false selon
    """
    proba=reu_actuel*10
    tirage=random.randint(0,100)
    return tirage<proba

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
    REQUEST_VARS['erreur_url'] = "erreur"
else:

    idp = REQUEST_VARS['url_components'][1]
    partie = recuperer_partie(connexion,idp)

    REQUEST_VARS['partie']= recompiler_partie(connexion,idp)
    if POST != {}:
        if 'case' in POST:
            action=POST['case'][0]
            regexp_pos = r'[0-9],[0-9]'
            pos_ok  = re.match(regexp_pos,action)
            if pos_ok:
                inserer_action(connexion,idp,action)
        else:
            REQUEST_VARS['erreur_action']="❌ Aucune case sélectionnée"
