'''urls de l'application users'''

from django.urls import path
from . import views

urlpatterns = [
	path('utilisateurs', views.utilisateurs, name='utilisateurs'),
	path('graph', views.graph, name = 'graph'),
]