def recuperer_partie(connexion, idp):
  """
    RENVOIE UN DICTIONNAIRE : PARTIE
  """
  query = """SELECT * FROM Partie WHERE idP = %s"""
  partie = select_query(connexion,query,[idp])

  if len(partie) == 0:
    print("aucune partie trouvé")
    return 404
  else:
    query = '''SELECT couleure FROM equipe WHERE nomE = %s'''

    print(partie)
    #select_query(connexion, query,[partie[0][i]])

    couleur = [select_query(connexion, query,[partie[0][i]])[0][0] for i in range(1,3)]

    tour = select_query(connexion,'SELECT MAX(numa) FROM Journal WHERE idp = %s',[idp])

    if tour[0][0] == None:
      tour = 1
    elif type(tour[0][0]) == int:
      tour = 2 if (tour[0][0] % 2 != 0) else 1

    print(partie)
    for k in partie:
        print(f"""{k}""")



    partie = {
      "nomE1":partie[0][1],
      "couleurE1": couleur[0],
      "nomE2":partie[0][2],
      "couleurE2": couleur[1],
      "idP":idp,
      "tour":tour,
      "grille":grille,
      "taille":partie[0][7],
      "max_tours":partie[0][6],
      "est_speciale":partie[0][10]
    }
    return partie
