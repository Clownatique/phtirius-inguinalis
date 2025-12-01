from model.partie import recompiler_partie
from model.partie import inserer_action, creer_partie, recompiler_partie, recuperer_partie
from model.utils import select_query

#pyright: reportUndefinedVariable=false

connexion = SESSION['CONNEXION']

def verifier_action(action:str,jouer:str, partie:list):
    """
        PRENDS:- un tuple de 2 cases
               - une manière d'identifier un jour (string ?)
         RENDS:- un bool pour le contrôleur
               - un str pour la bd si c bon/un message d'erreur
    """
    pos_sou = action[0].split(',')
    print(partie)
    print(pos_sou)
    if partie[int(pos_sou[0])][int(pos_sou[1])] == 0:
        return True
    else:
        return False
        # REQUEST_VARS[""]= "j'en connais un qui bidouille et ça me plaît pas"
        # return False

if not('url_components' in REQUEST_VARS):
    REQUEST_VARS['erreur'] = "erreur"
else:
    url_components = REQUEST_VARS['url_components']
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
        REQUEST_VARS['taille'] = partie['taille']
        REQUEST_VARS['joueur'] = REQUEST_VARS['partie'][f"""nomE{REQUEST_VARS['partie']['tour']}"""]
        if partie['est_speciale']:
            None
            #REQUEST_VARS['morpions'] = recuperer_morpions(connexion, nomE)

        if POST != {}:
            print(POST['case'])
            if verifier_action(POST['case'],REQUEST_VARS['joueur'], REQUEST_VARS['grille']):
                inserer_action(connexion,partie['idP'],POST['case'])
            #if verifier_action(POST['case'],REQUEST_VARS['jouer']):
#lig=int(form.get("ligne"))    ->
#col=int(form.get("colonne"))  -> avec le framework du prof, il faut utiliser le dictionnaire POST ;)
            #    inserer_action(connexion,idp, action)
            #else:
            # ici définir des REQUESTS_VARS['err'] # un tableau de message d'erreur
        #lig=int(form.get("ligne"))
        #col=int(form.get("colonne"))
