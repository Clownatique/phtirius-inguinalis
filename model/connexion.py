import psycopg

def get_connexion(host, username, password, db, schema):
    try:
        connexion = psycopg.connect(host=host, user=username, password=password, dbname=db, autocommit=True)
        cursor = psycopg.ClientCursor(connexion)
        cursor.execute("SET search_path TO %s", [schema])
    except Exception as e:
        print(e)
        return None
    return connexion
