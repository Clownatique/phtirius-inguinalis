import psycopg

connexion = SESSION['CONNEXION']

with connexion.cursor() as cursor:
    try:
        cursor.execute("SELECT image,pv,atk,mana,reu from morpion")
        result = cursor.fetchall()
        REQUEST_VARS['liste_morpion'] = result
        print(result)
    except psycopg.Error as e:
        print(f"Error : {e}")

if 'couleur' in POST: #si un des trucs a été fournis, afficher la réponse complète
    print(POST)
