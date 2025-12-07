from model.partie import inserer_action, recuperer_partie, terminer_partie,recompiler_partie
import re

connexion = SESSION['CONNEXION']

#pyright: reportUndefinedVariable=false

erreur_bool = not REQUEST_VARS.get('url_components')
erreur_bool = erreur_bool or(REQUEST_VARS['url_components'][0] == '')
erreur_bool = erreur_bool or recuperer_partie(connexion, REQUEST_VARS['url_components'][1]) == None
if erreur_bool:
    REQUEST_VARS['erreur'] = "erreur"
else:
# donnée à fournir QUOI QU'IL EN SOIT

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
