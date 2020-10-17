# projetWeb

Our project aims to design a website dedicated to our "Algorithm of Graphs" course.

The site is not accessible online, it is necessary to launch it locally using django.

We recommend installing a virtual environment to avoid any problems.

Our virtual environment being too heavy we cannot transfer it, here is the list of what it contains:

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


All this can be obtained via the "pip" command.

In addition, to be able to start the server locally it is necessary to install "PostgreSQL"
and enter the password ask during installation in the file:

/projet/settings.py

at DATABASES level, replace the line:
'PASSWORD': 'projetfac2018',
with 'PASSWORD': 'yourGreSQLPostPassword',

Once this is done, the server can be launche with the command:

"python manage.py runserver" (at the root of the project)

and the site is accessible at http://127.0.0.1:8000/.
(Do not use http: // localhost: 8000 / otherwise the exercise part will not work)
