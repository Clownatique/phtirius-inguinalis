from _typeshed import NoneType
import re
from model.equipe import insertion_equipe, insertion_posseder
from model.equipe import liste_morpion
from model.equipe import couleur_prises, noms_utilises

connexion = SESSION['CONNEXION']

# pyright: reportUndefinedVariable=false
REQUEST_VARS = {'nom':'','couleur':'','morpion':''}

def verif_morpion(morpions:list) -> bool:
    """
    Vérifie le bon nombre de morpion dans le form soumis
    Renvoie l'écart du nombre de morpion avec l'intervalle [6,8]
     # entre 6 et 8 : 0
     # plus de 8 : positif
     # moins de 6 : négatif
    """
    nombre_morpion = len(morpions)
    morpion_nec = max(0, min(nombre_morpion - 8, 6 - nombre_morpion))
    message = 'bon toutou'
    if morpion_nec > 0:
        message = f"""{champ} morpion(s) en trop.Enlevez en de votre équipe"""
    else:
        message = f"""{champ} morpion(s) en moins. Rajoutez en de votre équipe"""

    REQUEST_VARS['err_nombre_morpion'] = message
    if REQUEST_VARS == "bon toutou":
        return True
    return False



def verif_couleur_disponible(couleur:str) -> bool: # de tuples
    liste_coul_prises = []
    for _couleur in couleur_prises(connexion):
        liste_coul_prises.append(_couleur[0])
    if couleur in liste_coul_prises:
        REQUEST_VARS['err_couleur_indisponible'] = f'''{couleur} est déjà pris pr une autre équipe'''
        return False
    return True


def verif_nom_disponible(nom:str) -> bool:
    """
    Vérifie la disponibilité du nom d'équipe soumis
    Renvoie vrai si pris, faux si pas pris
    """
    noms_utilises_liste = [ i[0] for i in noms_utilises(connexion) ]
    if nom in noms_utilises_liste:
        REQUEST_VARS['err_nom_indisponible'] = f'''{nom} est déjà pris pr une autre équipe'''
        return False
    return True

def verif_nom_format(nom:str) -> bool:
    if len(nom) > 6:
        REQUEST_VARS['err_format_nom'] = f'''{nom} ne respecte pas le format demandé.'''
        return False
    return True

def verif_couleur_format(couleur:str) -> bool:
    regex = r'[0-9a-fA-F]{6}$'
    if not(bool(re.match(regex, couleur))): # j'ai utilisé de l'ia ici
        REQUEST_VARS['err_format_couleur'] = f'''{couleur} ne respecte pas le format demandé.'''

def verif_complet(post:dict) -> list:
    champ_manquant = []
    for champ in ['nom', 'couleur','morpions']:
        if not(champ in POST):
            champ_manquant.append(champ)
        else:
            REQUEST_VARS[champ] = post[champ]
    return champ_manquant

if POST != {}: # Si l'utilisateur a rentré des trucs
    REQUEST_VARS['tentative_creation_equipe'] = True
    champ_manquant = verif_complet(POST)

    if len(champ_manquant) == 0:

        couleur = POST['couleur'][0]
        nom = POST['nom'][0]
        morpions = POST['morpions']

        if (verif_complet(POST) and verif_morpion(morpions) and verif_couleur_disponible(couleur) and verif_couleur_format(couleur) and verif_nom_disponible(nom) and verif_nom_format(nom)):
            try:
                id_equipe_inseree =  insertion_equipe(connexion,nom,couleur)
                REQUEST_VARS['morpion_inseree'] = insertion_posseder(connexion,nom,couleur,morpions)
            except psycopg.Error as e:
                print(e)

    else:
        champ_existant = [champ for champ in champ_manquant if champ not in ['nom', 'couleur', 'morpions']]
        for champ in champ_existant:
            # pour quand même traiter les erreurs d'un utilisateur qui a oublié un champ
            if champ == 'couleur':
                couleur = POST['couleur'][0]
                verif_couleur_disponible()
                verif_couleur_format()
            if champ == 'nom':
                nom = POST['nom'][0]
                verif_nom_format(nom)
                verif_nom_disponible(nom)
            if champ == 'morpions':
                morpions = POST['morpions']
                verif_morpion(morpions)

        REQUEST_VARS['champ_manquant'] = champ_manquant

REQUEST_VARS['liste_morpion'] = liste_morpion(connexion)
