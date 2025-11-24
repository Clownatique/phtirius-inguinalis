"""
Ficher initialisation (eg, constantes chargées au démarrage dans la session)
"""
from datetime import datetime
from os import path
from tomllib import load
from model.connexion import get_connexion


SESSION['APP'] = "Morpion"
SESSION['BASELINE'] = "Critiquez vos séries !"
SESSION['DIR_HISTORIQUE'] = path.join(SESSION['DIRECTORY'], "historiques")
SESSION['HISTORIQUE'] = dict()
SESSION['CURRENT_YEAR'] = datetime.now().year

try:
    with open('config-bd.toml', 'rb') as fp:
        config = load(fp)
except Exception as e:
    print(f"Erreur lors de la lecture du fichier: {e}")

connexion = get_connexion(config['POSTGRESQL_SERVER'],config['POSTGRESQL_USER'],config['POSTGRESQL_PASSWORD'],config['POSTGRESQL_DATABASE'],'morpion')

try:
    with open('rendu/schema.sql', 'rb') as sql_buff:
        with connexion.cursor() as cursor:
            cursor.execute(sql_buff.read())

except Exception as e:
    print(f"Erreur lors du peuplement de la base de donné: {e}")


SESSION['CONNEXION'] = connexion
