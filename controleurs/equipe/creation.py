import psycopg
import re
from model.equipe import insertion_equipe, insertion_posseder
from model.equipe import liste_morpion
from model.equipe import couleur_prises, noms_pris

connexion = SESSION['CONNEXION']

def verif_nombre_morpion(equipe_dict:dict) -> int:
    """
    Vérifie le bon nombre de morpion dans le form soumis
    Renvoie l'écart du nombre de morpion avec l'intervalle [6,8]
     # entre 6 et 8 : 0
     # plus de 8 : positif
     # moins de 6 : négativ
    """
    if not('morpion' in equipe_dict):
        return 6
    nombre_morpion = len(equipe_dict['morpion'])
    return max(0, min(nombre_morpion - 8, 6 - nombre_morpion))

def couleur_est_pris(equipe_dict:dict) -> bool: # de tuples
    couleur_voulu = equipe_dict['couleur'][0]
    liste_coul_prises = []
    for i in couleur_prises(connexion):
        liste_coul_prises.append(i[0])
    print(liste_coul_prises)
    return couleur_voulu in liste_coul_prises


def verif_nom_pris(equipe_dict:dict) -> bool :
    """
    Vérifie la disponibilité du nom d'équipe soumis
    Renvoie vrai si pris, faux si pas pris
    """
    liste_coul_prises = [ i[0] for i in noms_pris(connexion) ]
    print(equipe_dict['nom'])
    print(liste_coul_prises)
    if equipe_dict['nom'][0] in liste_coul_prises:
        print("le nom est pris")
    return equipe_dict['nom'][0] in liste_coul_prises

def couleur_format(equipe_dict:dict) -> bool:
    couleur = equipe_dict['couleur'][0]
    regex = r'[0-9a-fA-F]{6}$'
    return not(bool(re.match(regex, couleur))) # j'ai utilisé de l'ia ici

if POST != {}: # Si l'utilisateur a rentré le formulaire
    REQUEST_VARS['tentative_creation_equipe'] = True
    REQUEST_VARS['couleurE'] = POST['couleur'][0]
    REQUEST_VARS['nomE'] = POST['nom'][0]
    dispo_couleur = couleur_est_pris(POST)
    dispo_nom = verif_nom_pris(POST)
    nombre_morpion = verif_nombre_morpion(POST)
    couleur_format_ok = couleur_format(POST)
    print(f"""dispo_nom:{dispo_nom},dispo_couleur:{dispo_couleur},couleur_format_ok:{couleur_format_ok}""")
    print(POST)
    if ('morpion' in POST or 'nom' in POST or 'couleur' in POST):
        print('aya l"user a pas tout mis')
    if ( len(POST['nom']) > 6 or dispo_couleur or dispo_nom or nombre_morpion != 0 or couleur_format_ok):
        if len(POST['nom']) > 6:
            REQUEST_VARS["err_taille_nom"] = f'''{REQUEST_VARS['nom']} est un nom d\'équipe bien trop long'''


        REQUEST_VARS['err_couleur_format'] = not(couleur_format)
        REQUEST_VARS['err_nom_indisponible'] = dispo_nom
        REQUEST_VARS['err_couleur_indisponible']= dispo_couleur
        REQUEST_VARS['err_format_couleur'] = couleur_format_ok
        if nombre_morpion <0:
            print("en moins")
            REQUEST_VARS['err_nb_morpion'] = f"""{nombre_morpion} morpion(s) en trop.Enlevez en de votre équipe"""
        elif nombre_morpion > 0:
            print("en trop")
            REQUEST_VARS['err_nb_morpion'] = f"""{nombre_morpion} morpion(s) en moins. Rajoutez en de votre équipe"""
        else:
            REQUEST_VARS['err_nb_morpion'] = nombre_morpion
        print("eh oui y'a des erreurs")
    else:
        try:
            id_equipe_inseree =  insertion_equipe(connexion,POST['nom'],POST['couleur'])
            REQUEST_VARS['morpion_inseree'] = insertion_posseder(connexion, POST['nom'],POST['couleur'], POST['morpion'])
        except psycopg.Error as e:
            print(e)

REQUEST_VARS['liste_morpion'] = liste_morpion(connexion)
