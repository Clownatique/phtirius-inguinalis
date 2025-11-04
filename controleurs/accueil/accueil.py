from model.utils import requete_bete

REQUEST_VARS['test'] = requete_bete(SESSION['CONNEXION'],'SELECT CURRENT_DATABASE()')
