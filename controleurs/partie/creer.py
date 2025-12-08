import psycopg
from model.equipe import liste_equipes
from model.partie import creer_partie

#pyright: reportUndefinedVariable=false
#pour ne pas prendre les erreurs des variables non déclarées

connexion = SESSION['CONNEXION']
REQUEST_VARS["equipes"] = liste_equipes(connexion)

def verif_formulaire(post:dict) -> bool:
    """

    """
    #renvoie permets d'afficher toutes les erreurs avant le refus du form
    renvoie = True
    if not('nome1'in post and 'nome2' in post):
        REQUEST_VARS['err_nb_equipes'] = "Vous DEVEZ choisir exactement 2 équipe"
        renvoie = False
    else:
        if post["nome1"] == post["nome2"]:
            REQUEST_VARS['err_meme_equipe'] = "Vous ne pouvez pas faire affronter la même équipe"
            renvoie = False

    if not('nb_tour_max' in post):
        REQUEST_VARS['err_nb_tour'] = "Vous devez choisir un nombre tour, petit malin"
        renvoie = False
    else:
        if int(post['nb_tour_max'][0]) > int(post['taille_grille'][0])**2:
            REQUEST_VARS['att_nb_tour_absurde'] = "! vous avez mis un nombre d'action bien trop grand (et c ok)"
            renvoie = False
        if int(post['nb_tour_max'][0]) < 0 or int(post['nb_tour_max'][0]) == 0:
            REQUEST_VARS['err_nb_tour'] = "vous devez rentrer un nombre de tour (positif) on fait un morpion et toi tu testes des valeurs absurdes"
            renvoie = False

    if not('taille_grille' in post):
        REQUEST_VARS['err_taille_grille'] = "Vous devez choisir une taille grille ! en plus on se casse la tête à faire des grilles qui peuvent être grandes ??"
        renvoie = False
    else:
        if int(post['taille_grille'][0]) > 65:
            REQUEST_VARS['err_taille_grille'] = "faut pas pousser mémé (on fait tourner le tout sur un rpi)"
            renvoie = False
    return renvoie

if POST != {}:
    REQUEST_VARS['partie_soumise'] = True

    est_speciale = True if 'est_speciale' in POST else False
    # pour l'instant je n'arrive pas à récupérer l'input "radio" du champ "est_speciale"

    if verif_formulaire(POST):
        try:
            creer_partie(connexion,POST["nome1"][0], POST["nome2"][0],est_speciale,int(POST['nb_tour_max'][0]),int(POST['taille_grille'][0]))
        except psycopg.Error as e:
            print({e})
