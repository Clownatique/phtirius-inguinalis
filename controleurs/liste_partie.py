from model.utils import get_instances

connexion = SESSION['CONNEXION']

REQUEST_VARS['liste_partie'] = get_instances(connexion, "partie")
