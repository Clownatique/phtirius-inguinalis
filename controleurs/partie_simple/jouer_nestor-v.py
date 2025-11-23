from model.partie import inserer_action, creer_partie, recompiler_partie

connexion = SESSION['CONNEXION']
#idP = recuperer_partie
idP = ['equipe_1','equipe_2','couleur_1', 'couleur_2']
recompiler_partie(connexion, idP)

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
  inserer_action(idP,texte) #a faire?

  return {
    "succes":True,
    "grille": partie["grille"]
  }

from model.partie import recompiler_partie,verifier_action

#REQ

REQUEST_VARS['partie'] = {"nomE1":"équipe 1", "nomE2":"équipe 2", "couleurE1":"#eeefff", "couleurE2":"#cccaaaa"}
REQUEST_VARS['grille'] = [[],[],[]]



if POST != {}:
