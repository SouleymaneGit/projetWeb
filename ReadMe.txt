Projet Web :

Notre projet a pour pour but de concevoir un site web dédié au cours d’Algorithme des graphes. 

Le site n'étant pas accessible en ligne il est nécessaire de le lancer en local grâce à django.

Nous conseillons d'installer un environnement virtuel pour éviter tous problèmes.

Notre environnement virtuel étant trop lourd nous ne pouvons le transférer, voici la liste de ce qu'il contient :

decorator 4.3.0
Django 2.0.5
networkx 2.1
nose 1.3.7
numpy 1.14.3
pip 10.0.1
psycopg2 2.7.4
pytz 2018.4
PyYAML 3.12
scipy 1.1.0
setuptools 39.2.0
wheel 0.31.1

Tout cela est obtenable via la commande "pip".

De plus pour pouvoir lancer le serveur localement il est nécessaire d'installer PostgreSQL
et de rentrer le mot de passe demander lors de l'installation dans le fichier :

/projet/settings.py

au niveau de DATABASES, remplacer la ligne :
'PASSWORD': 'projetfac2018',
par 'PASSWORD': 'votreMotDePassePostGreSQL',

Une fois cela effectué le serveur ce lance grâce à la commande :

"python manage.py runserver" (à la racine du projet)

et le site est accessible à l'adresse http://127.0.0.1:8000/ .
(Ne pas utiliser http://localhost:8000/ sinon la partie exercice ne fonctionnera pas)