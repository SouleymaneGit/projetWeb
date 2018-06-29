from django.http import HttpResponse
from django.shortcuts import render
from users.randomGraph import *

# Create your views here.

def utilisateurs(request) :
	'''vue qui retourne la page d'un utilisateur'''
	return render(request, 'users/utilisateurs.html')
	
def graph(request):
	typeExercice = request.GET.get('typeExercice', None)
	data = randomGraph(typeExercice)
	return HttpResponse(data)