'''urls de l'application signin_up'''

from django.urls import path
from . import views

urlpatterns = [
	path('', views.accueil, name='accueil'),
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('home/', views.HomePageView.as_view(), name='home'),
]