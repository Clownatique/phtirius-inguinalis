import psycopg
# from .equipe import insertion_equipe, insertion_posseder
# from .equipe import liste_morpion

connexion = SESSION['CONNEXION']

# fonction qui restent ici

def verif_nombre_morpion(equipe_dict:dict) -> int:
    ""
    "" # entre 6 et 8 : 0
    "" # plus de 8 : positif
    "" # moins de 6 : négativ
    ""
    None

def verif_dispo_nom_equipe(connexion,equipe_dict:dict) -> bool :
    ""
    "" #on fait requêtes
    ""
    None
    
def verif_dispo_couleur_equipe(connexion, equipe_dict:dict) -> bool:
    None

def verif_couleur_format(equipe_dict:dict) -> bool:
    None

if POST != {}: # Si l'utilisateur a rentré le formulaire
    print('la lumiere fut')
    # pour afficher l'encart avec le message de réussite de l'envoie du form
    REQUEST_VARS['tentative_creation_equipe'] = True
    REQUEST_VARS['couleurE'] = POST['couleur'][0]
    REQUEST_VARS['nomE'] = POST['nom'][0] 
    # appel aux fonctions de vérif

    dispo_couleur = verif_dispo_couleur_equipe(connexion,POST)
    dispo_nom = verif_dispo_nom_equipe(connexion,POST)
    nombre_morpion = verif_nombre_morpion(POST)
    couleur_format = verif_couleur_format(POST)
    # déf des messages d'erreur côté utilisateur
    print(nombre_morpion)
    if couleur_format != True:
        REQUEST_VARS['couleur_format'] = False
    if dispo_couleur or dispo_nom:
        REQUEST_VARS['nom_indisponible'] = dispo_nom
        REQUEST_VARS['couleur_indisponible']= dispo_couleur

    if nombre_morpion != None: 
        if nombre_morpion > 0:
            REQUEST_VARS['erreur_nb_morpion'] = f"""{nombre_morpion} morpion(s) en trop.Enlevez en de votre équipe"""
        elif nombre_morpion < 0:
            REQUEST_VARS['erreur_nb_morpion'] = f"""{nombre_morpion} morpion(s) en moins. Rajoutez en de votre équipe"""
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


