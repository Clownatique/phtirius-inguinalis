from model.statistiques import (
    compter_instances,
    top_3_equipes,
    parties_extremes,
    moyenne_journal_par_mois,
    formater_duree
)

# pyright: reportUndefinedVariable=false

connexion=SESSION['CONNEXION']

#on récupère les stats :

#nb d'instances dans 3 tables:
REQUEST_VARS['stats_instances']=compter_instances(connexion)

#top 3 des equipes avec le plus de victoires
REQUEST_VARS['top_equipes']=top_3_equipes(connexion)

#partie la plus rapide et la plus longue
parties_stats=parties_extremes(connexion)
REQUEST_VARS['partie_rapide']=parties_stats.get('rapide')
REQUEST_VARS['partie_longue']=parties_stats.get('longue')

#moyenne de lignes de journal par mois/annee
journal_stats=moyenne_journal_par_mois(connexion)
REQUEST_VARS['journal_mois']=journal_stats

#fonction qui aide à formater les durées dans le template
REQUEST_VARS['formater_duree']=formater_duree
