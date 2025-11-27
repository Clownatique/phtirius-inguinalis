from model.partie import recompiler_partie
from model.partie import inserer_action, creer_partie, recompiler_partie, recuperer_partie
from model.utils import select_query

#pyright: reportUndefinedVariable=false

def verifier_action(case:tuple,joueur:str):
    """
        PRENDS:- un tuple de 2 cases
               - une manière d'identifier un jour (string ?)
         RENDS:- un bool pour le contrôleur
               - un str pour la bd si c bon/un message d'erreur
    """
    return True


#url_components = REQUEST_VARS['url_components']
url_components = [None,'903843bd-2f39-4a82-adb3-13bd99c1f932']
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
        REQUEST_VARS['joueur'] = REQUEST_VARS['partie'][f"""nomE{REQUEST_VARS['partie']['tour']}"""]
        if partie['est_speciale']:
            None
            #REQUEST_VARS['morpions'] = recuperer_morpions(connexion, nomE)

        if POST != {}:
            print(POST['case'])
            #if verifier_action(POST['case'],REQUEST_VARS['jouer']):
#lig=int(form.get("ligne"))    ->
#col=int(form.get("colonne"))  -> avec le framework du prof, il faut utiliser le dictionnaire POST ;)
            #    inserer_action(connexion,idp, action)
            #else:
            # ici définir des REQUESTS_VARS['err'] # un tableau de message d'erreur
        #lig=int(form.get("ligne"))
        #col=int(form.get("colonne"))
