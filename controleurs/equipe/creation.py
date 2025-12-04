import re
from model.equipe import insertion_equipe, insertion_posseder
from model.equipe import liste_morpion
from model.equipe import couleur_prises, noms_utilises

connexion = SESSION['CONNEXION']

# pyright: reportUndefinedVariable=false
#REQUEST_VARS = {'nom':'','couleur':'','morpion':''}

REQUEST_VARS["liste_morpion"] = liste_morpion(connexion)

def verif_morpion(morpions:list) -> bool:
    """
    Vérifie le bon nombre de morpion dans le form soumis
    Renvoie l'écart du nombre de morpion avec l'intervalle [6,8]
     # entre 6 et 8 : 0
     # plus de 8 : positif
     # moins de 6 : négatif
    """
    nombre_morpion = len(morpions)
    morpion_nec = max(0, max(nombre_morpion - 8, 6 - nombre_morpion))
    if nombre_morpion < 6:
        REQUEST_VARS['err_nombre_morpion'] = f"""{morpion_nec} morpion(s) en moins. Rajoutez-en dans votre équipe"""
    if nombre_morpion >8 :
        REQUEST_VARS['err_nombre_morpion'] = f"""{morpion_nec} morpion(s) en trop. Enlevez-en dans votre équipe"""

    if morpion_nec==0:
        REQUEST_VARS['succes'] = "Equipe créée !"
        return True
    return False

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
    regex = r'^[0-9a-fA-F]{6}$'
    # bien si on le fait sans regexp
    if not(bool(re.search(regex, couleur))): # j'ai utilisé de l'ia ici
        REQUEST_VARS['err_format_couleur'] = f'''{couleur} ne respecte pas le format demandé.'''
        return False
    return True

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

        if  (verif_morpion(morpions) and verif_couleur_format(couleur) and verif_nom_disponible(nom) and verif_nom_format(nom)):
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
                verif_couleur_format(couleur)
            if champ == 'nom':
                nom = POST['nom'][0]
                verif_nom_format(nom)
                verif_nom_disponible(nom)
            if champ == 'morpions':
                morpions = POST['morpions']
                verif_morpion(morpions)

        REQUEST_VARS['champ_manquant'] = champ_manquant

REQUEST_VARS["liste_morpion"] = liste_morpion(connexion)
print(liste_morpion(connexion))
