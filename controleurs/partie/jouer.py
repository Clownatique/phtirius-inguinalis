from model.partie import recompiler_partie,verifier_action
from model.partie import inserer_action, creer_partie, recompiler_partie, recuperer_partie
from model.utils import select_query

#pyright: reportUndefinedVariable=false
url_components = REQUEST_VARS['url_components']
connexion = SESSION['CONNEXION']

if url_components[1] == '':
    REQUEST_VARS['erreur'] = "erreur"
else:
    idp = url_components[1]
    connexion = SESSION['CONNEXION']
    partie = recuperer_partie(connexion,idp)
    if partie == 404:
        REQUEST_VARS['erreur'] = "erreur"
    else:
        REQUEST_VARS['partie'] = partie
        print(partie)
        REQUEST_VARS['grille'] = recompiler_partie(connexion,partie['idP'])
        REQUEST_VARS['avancee'] = partie['est_speciale']
        REQUEST_VARS['taille'] = 3
        REQUEST_VARS['joueur'] = 0
        if partie['est_speciale']:
            None
            #REQUEST_VARS['morpions'] = recuperer_morpions(connexion, nomE)

        #if POST != {}:

        #lig=int(form.get("ligne"))
        #col=int(form.get("colonne"))
        #uery = """SELECT * FROM Partie"""
