import psycopg
import re
from model.equipe import insertion_equipe, insertion_posseder
from model.equipe import liste_morpion
from model.equipe import couleur_prises, noms_pris
# from model.flora import liste_morpion

connexion = SESSION['CONNEXION']

# fonction qui restent ici

def verif_nombre_morpion(equipe_dict:dict) -> int:
    """
    Vérifie le bon nombre de morpion dans le form soumis
    Renvoie l'écart du nombre de morpion avec l'intervalle [6,8]
     # entre 6 et 8 : 0
     # plus de 8 : positif
     # moins de 6 : négativ
    """
    nombre_morpion = len(equipe_dict['morpion'])
    return max(0, min(nombre_morpion - 8, 6 - nombre_morpion))

def verif_nom_pris(equipe_dict:dict) -> bool :
    """
    Vérifie la disponibilité du nom d'équipe soumis
    Renvoie vrai si pris, faux si pas pris
    """
    nom_pris = noms_pris()
    couleur = equipe_dict['couleur']
    return couleur in nom_pris
    
def couleur_format(equipe_dict:dict) -> bool:
    couleur = equipe_dict['couleur']
    regex = r'^#[0-9a-fA-F]{6}$'
    return bool(re.match(regex, couleur)) # j'ai utilisé de l'ia ici

if POST != {}: # Si l'utilisateur a rentré le formulaire
    print('la lumiere fut')
    # pour afficher l'encart avec le message de réussite de l'envoie du form
    REQUEST_VARS['tentative_creation_equipe'] = True
    REQUEST_VARS['couleurE'] = POST['couleur'][0]
    REQUEST_VARS['nomE'] = POST['nom'][0] 
    # appel aux fonctions de vérif

    dispo_couleur = couleur_prises(SESSION['CONNEXION'],POST)
    dispo_nom = verif_nom_pris(POST)
    nombre_morpion = verif_nombre_morpion(POST)
    couleur_format = couleur_format(POST)
    # déf des messages d'erreur côté utilisateur
    print(nombre_morpion)
    if couleur_format != True:
        REQUEST_VARS['err_couleur_format'] = False
    if dispo_couleur or dispo_nom:
        REQUEST_VARS['err_nom_indisponible'] = dispo_nom
        REQUEST_VARS['err_couleur_indisponible']= dispo_couleur

    if nombre_morpion != None: 
        if nombre_morpion > 0:
            REQUEST_VARS['err_nb_morpion'] = f"""{nombre_morpion} morpion(s) en trop.Enlevez en de votre équipe"""
        elif nombre_morpion < 0:
            REQUEST_VARS['err_nb_morpion'] = f"""{nombre_morpion} morpion(s) en moins. Rajoutez en de votre équipe"""
        else:
            print("erreur : valeur de renvoi de verif_nombre_morpionincohérente")
            #j'ai oublié comment on assert

    # si tout est bon, on essaie d'entrer l'équipe en esperant que postgre
    # lache pas

    try:
        equipe_insertion()
        posseder_insertion()
    except:
       REQUEST_VARS['erreur_insertion'] = "erreur_insertion"# ici l'erreur est uniquement dûe à la
       # base de données

else: # Si l'utilisateur a besoin du formulaire
   None 
with connexion.cursor() as cursor:
    try:
        cursor.execute("SELECT image,pv,atk,mana,reu from morpion")
        result = cursor.fetchall()
        REQUEST_VARS['liste_morpion'] = result
    except psycopg.Error as e:
        print(f"Error : {e}")


