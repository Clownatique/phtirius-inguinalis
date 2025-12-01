def recompiler_partie(connexion, idP):
  """
    Renvoie un tableau correspondant à la partie passé en paramètre
  """
  sel_partie = """WHERE idp = %s"""
  query = f"""SELECT * FROM journal {sel_partie} ORDER BY numA DESC"""
  actions = select_query(connexion,query, [idP])
  query = """SELECT taille_grille FROM partie """+sel_partie
  taille_grille = select_query(connexion, query,[idP])[0][0]
  print(f'''action joué durant la partie {idP}:{actions}''')
  if taille_grille == None:
    taille_grille = 3

  grille = [[0 for _ in range(taille_grille)] for _ in range(taille_grille)]
  # 0 : case vide
  # None : case détruite
  # 'idM' : morpion avancé dessus
  # 1/2 : partie simple

  for i in actions:
    # une action dans le contexte d'une partie simple ça ressemble à ça:
    # (0 ou 1): x,y
    # pour l'instant les grilles ne peuvent pas aller au dessus de 9
    print(f"action:{i}")
    x = int(i[1][:1])
    y = int(i[1][2:])
    grille[x][y] = 1 if i[0] % 2 != 0 else 2

  return grille

def verifier_action(connexion, grille:list, action):
  # coup illégal : placer un pion alors qu'il y'en a déjà un
  x = action[2:-2]
  y = action[4:]
  if partie['grille'][x][y]:
    return False
  return True
