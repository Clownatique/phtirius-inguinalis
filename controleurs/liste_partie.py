from model.utils import get_instances

connexion = SESSION['CONNEXION']

REQUEST_VARS['liste_partie'] = get_instances(connexion, "partie")
for i in range(len(REQUEST_VARS['liste_partie'])):
    print(REQUEST_VARS['liste_partie'][i])
