from model.partie import inserer_action, terminer_partie
from model.partie import recompiler_partie_avancee, recuperer_morpions_joueur
import re

connexion = SESSION['CONNEXION']

#pyright: reportUndefinedVariable=false

erreur_bool = not REQUEST_VARS.get('url_components')
erreur_bool = erreur_bool or(REQUEST_VARS['url_components'][0] == '')
if erreur_bool:
    REQUEST_VARS['erreur'] = "erreur"
else:
    idp = REQUEST_VARS['url_components'][1]
    if idp == None:
        idp = 0
    partie = recompiler_partie_avancee(connexion,idp)
    REQUEST_VARS['partie'] = partie
    REQUEST_VARS['nomEJ'] = partie[f"nomE{partie['joueur']}"]
    if POST != {}:
        if 'case' in POST:
            #d'abord on vérifie si l'action c un placement
            if 'action' in POST:
                case = POST['case'][0]
                action = POST['action'][0]
                if not(action[0].isalpha()):
                    # donc c un placement dans partie avancé
                    action = f"{case}<{action}"
                else:
                    action = f"{action}>{case}"


                regexp_sort = r'(sn|bf|ag|at):([0-9],[0-9])(<|>)([0-9],[0-9])'
                regexp_pos = r'[0-9],[0-9]<[0-9]+'

                sort_ok = re.match(regexp_sort,action)
                pos_ok  = re.match(regexp_pos,action)
                if  pos_ok != None or sort_ok != None:
                    inserer_action(connexion,idp, action)
                else:
                    print('que ça bidouille')
        else:
            REQUEST_VARS['erreur_action']="❌ Aucune case sélectionnée"
