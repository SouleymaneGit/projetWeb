from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

# Create your views here.

def accueil(request) :
	'''vue qui retourne la page d'accueil du site'''
	return render(request, 'signin_up/accueil.html')
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
class HomePageView(TemplateView):
    template_name = 'home.html'