from model.partie import recup_equipe

connexion = SESSION['CONNEXION']

grille = [[{
    'nom':'morpion_2',
    'image':'t1.png',
    'mana':12,
    'pv':7,
    'reu':9,
    'atk':4
},{},{}],[{
    'nom':'morpion_1',
    'image':'t3.png',
    'mana':13,
    'pv':5,
    'reu':11,
    'atk':1
},{},{}],[{},{},{}]]

REQUEST_VARS['partie']={
    'nomE1': 'Tigers',
    'couleurE1': 'ececec',
    'nomE2': 'Dragons',
    'couleurE2': 'dadada',
    'idP': '903843bd-2f39-4a82-adb3-13bd99c1f932',
    'grille':grille,
    'equipee1':recup_equipe(connexion, 'Tigers'),
    'equipee2':recup_equipe(connexion, 'Dragons'),
    'tour': 1,
    'taille': 3,
    'est_speciale': True
}

if POST != {}:
    None
