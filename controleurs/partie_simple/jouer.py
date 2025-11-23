from model.partie import inserer_action, creer_partie

def afficher_tour(idP, numTour):
  #charge les informations nécessaires pour afficher le tour courant (grille, equipe qui doit jouer, liste des morpions dispo)
  partie=creer_partie(idP) #ou faire une fonction qui charge la partie ?
  return{
    "partie": partie,
    "grille": partie["grille"],
    "joueur_courant": partie["joueur_courant"],
    "numero_tour": numero_tour,
    "morpions": partie["morpions_jouables"]
  }


#lorsque le joueur essaie de placer un morpion, form contient : idMorpion, ligne, colonne
def action_placer_morpion(idP, form):
  morpion=int(form.get("idM"))
  lig=int(form.get("ligne"))
  col=int(form.get("colonne"))

  partie=charger_partie(idP) #a faire?

  if partie["grille"][lig][col] is not None :
    return {"erreur": "La case est déjà occupée."}

  partie["grille"][lig][col]=morpion
  texte=f"Le morpion {morpion} a été placé en ({lig},{col})."
  enregistrer_action(idP,texte) #a faire?

  return {
    "succes":True,
    "grille": partie["grille"]
  }
  
