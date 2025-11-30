from datetime import datetime
from os import path
from tomllib import load
from model.connexion import get_connexion


SESSION['APP'] = "Morpion"
SESSION['BASELINE'] = "Jouez au morpion"
SESSION['DIR_HISTORIQUE'] = path.join(SESSION['DIRECTORY'], "historiques")
SESSION['HISTORIQUE'] = dict()
SESSION['CURRENT_YEAR'] = datetime.now().year

try:
    with open('config-bd.toml', 'rb') as fp:
        config = load(fp)

    connexion = get_connexion(config['POSTGRESQL_SERVER'],config['POSTGRESQL_USER'],config['POSTGRESQL_PASSWORD'],config['POSTGRESQL_DATABASE'],'morpion')

    SESSION['CONNEXION'] = connexion
    with connexion.cursor() as cursor:
        try:
            with open('rendu/schema.sql', 'rb') as sql_buff:
                cursor.execute(sql_buff.read())

        except Exception as e:
            print(f"Erreur lors de la création de la bd: {e}")

        try:
            with open('rendu/peuplement.sql', 'rb') as sql_buff:
                cursor.execute(sql_buff.read())

        except Exception as e:
            print(f"Erreur lors du peuplement de la bd:{e}")

except Exception as e:
    print(f"Erreur lors de la lecture du fichier: {e}")
