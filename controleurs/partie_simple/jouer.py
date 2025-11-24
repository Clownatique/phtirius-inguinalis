from model.partie import recompiler_partie,verifier_action
from model.partie import inserer_action, creer_partie, recompiler_partie

#connexion = SESSION['CONNEXION']
#idP = recuperer_partie
#idP = ['equipe_1','equipe_2','couleur_1', 'couleur_2']
#recompiler_partie(connexion, idP)
#morpion=int(form.get("idM"))
#lig=int(form.get("ligne"))
#col=int(form.get("colonne"))

#partie = {
#   "partie": partie,
#   "grille": partie["grille"],
#   "joueur_courant": partie["joueur_courant"],
#   "numero_tour": numero_tour,
#   "morpions": partie["morpions_jouables"]
# }

REQUEST_VARS['partie'] = {"nomE1":"équipe 1", "nomE2":"équipe 2", "couleurE1":"#eeefff", "couleurE2":"#cccaaaa"}
REQUEST_VARS['grille'] = [[],[],[]]
REQUEST_VARS['joueur'] = 0
REQUEST_VARS['taille'] = 3

if POST != {}:
