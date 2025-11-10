from model.utils import requete_bete
from model.utils import requete_simple 

REQUEST_VARS['jul'] = requete_bete(SESSION['CONNEXION'],'SELECT * FROM morpion;')

# le mr a dit : de se partager les fontions du modele
# le bon vieil ami excel si jamais c compliqué
# drop table, create table, insert table

# si le morpion est un template, comment retrouver le morpion utilisé dans la
# partie X ?
#
# faire le plus simple possible (C PAS INDIQUE POUR UNE BONNE RAISON)
#
# revoir le sens des cardinalitéso
#
# askip pas très grave : la non présence de idP
#
# looping
#
# configuration daté se fait pas comme en td
