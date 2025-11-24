from model.partie import recompiler_partie,verifier_action
from model.partie import inserer_action, creer_partie, recompiler_partie, recuperer_partie
from model.utils import select_query

url_components = REQUEST_VARS['url_components']
print(url_components)

if url_components[1] == '':
    REQUEST_VARS['erreur'] = "erreur"
else:
    idp = url_components[1]
    connexion = SESSION['CONNEXION']
    partie = recuperer_partie(connexion,idp)
    if partie == None:
        REQUEST_VARS['erreur']
    #idP = ['equipe_1','equipe_2','couleur_1', 'couleur_2']
    #recompiler_partie(connexion, idP)
    #morpion=int(form.get("idM"))
    #lig=int(form.get("ligne"))
    #col=int(form.get("colonne"))

    #partie = {
    #   "partie": partie,
    #   "grille": partie["grille"],
    #   "joueur_courant": partie["joueur_courant"],
    #   "numero_tour": numero_tour,
    #   "morpions": partie["morpions_jouables"]
    # }



    partie = recuperer_partie(connexion, idp)
    print(partie)
    REQUEST_VARS["partie"] = recuperer_partie(connexion, idp)
    REQUEST_VARS['grille'] = [None, None, None]
    REQUEST_VARS['joueur'] = 0
    REQUEST_VARS['taille'] = 3

    #if POST != {}:

    query = """SELECT * FROM Partie"""
    print("liste_partie:")
    print(select_query(connexion,query))
