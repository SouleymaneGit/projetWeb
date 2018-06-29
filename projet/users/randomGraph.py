"""
	Module permettant la génération d'exercice au format json sur l'algorithmique des graphes

	Comment créer un exercice :
		Chaque fonction générant un exercice doit être composé :
		- d'une question : "question": "string"

		- d'un graph (pertinent en fonction de la question) : au format json (avec un id pour chaque arc)

		- d'un paramètre directed : "directed": "True/False"

		- d'un paramètre ponderate : "ponderate": "True/False"

		- d'un paramètre true_answer : "true_answer": "String/Tableau de noeuds/etc ..."

		- d'un paramètre wrong_answer : "wrong_answer": "3 String séparé par le caractère 'z' "

		- d'un paramètre colorbase : "colorbase": "Tableau de noeuds a coloré à l'affichage de la question/None"

		- d'un paramètre colorreponse : "colorreponse": "{..."
			- contenant "nodes:" "{ensemble de noeuds}",
			- contenant "edges:" "{ensemble d'arcs}" }
			une couleur peut être fournit devant les noeuds ou arcs pour les colorer de cette couleur

		- d'un paramètre complementreponse : "complementreponse": "String apportant une information à la bonne réponse/None"

		Tout ces paramètres doivent être inclue en une seule variable au format json pour être renvoyé au script

		exemple :

		{ "question": "Combien de composantes fortement connexes possède ce graph ?", "ponderate": "False", "colorbase": "None",
		 "colorreponse": {"nodes": "{yellow,4,red,6,green,0,orange,2,pink,1,purple,3,white,5,brown,7}"}, "complementreponse": "None",  
		 "directed": "True", "multigraph": "False", "graph": {}, "nodes": [{"id": 0}, {"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}, {"id": 7}], 
		 "links": [{"id": 0, "source": 0, "target": 6}, {"id": 1, "source": 1, "target": 2}, {"id": 2, "source": 6, "target": 4}, {"id": 3, "source": 7, "target": 1}], 
		 "true_answer": "8", "wrong_answer": "8z10z9z"}

		La fonction ainsi créé doit être inclus dans la fonction randomGraph(typeExercice).
"""


import networkx as nx
import random
from networkx.algorithms.approximation import clique
from networkx.algorithms.cycles import find_cycle

listColor = ["yellow", "#ff0210", "#1AD723", "orange", "pink", "#b302d7", "white", "#45a9d7"]
colorBonneReponse = "yellow"
colorMauvaiseReponse = "#ff0210"

def randomGraph(typeExercice):
	""" 
		Génere un exercice sur l'agorithmie des graphs au format json : 
		- question + graph + reponses + info diverses
		
		l'exercice générer dépend du paramètre 'typeExercice' :
		- "dijsktra" ou "bellmanford" ou "clique" ou "random
	"""
	if(str(typeExercice) == "dijkstra"):

		randomDijkstra = random.randint(1,4)

		if(randomDijkstra < 4):
			return dijkstraGraph()
		else:
			return negatifDijkstra()

	elif(str(typeExercice) == "bellmanford"):

		return bellmanFord()

	elif(str(typeExercice) == "clique"):

		return cardinalMaxClique()

	elif(str(typeExercice) == "acm"):

		return arbreCouvrantMinimal()

	elif (str(typeExercice) == "cfc"):

		return composanteFortementConnexe()

	else:
		questionRandom = random.randint(1,12)

		if(questionRandom <= 3):
			return dijkstraGraph()
		elif(questionRandom == 4):
			return negatifDijkstra()
		elif(questionRandom == 5 or questionRandom == 6):
			return cardinalMaxClique()
		elif(questionRandom == 7 or questionRandom == 8):
			return bellmanFord()
		elif(questionRandom == 9 or questionRandom == 10):
			return arbreCouvrantMinimal()
		elif(questionRandom == 11 or questionRandom == 12):
			return composanteFortementConnexe()
		else:
			return 0


def graphToJson(G):
	""" transformation d'un graph au format json """

	graph = nx.node_link_data(G) #transformation au format json
	jsonData = str(graph).replace("\'","\"").replace("True","\"True\"").replace("False","\"False\"") #correction du format json

	return jsonData


def addWeight(G):
	""" prend un graph en paramètre ajoute des poids de 1 à 8 sur ces arcs  """
	for e in G.edges():
		G[e[0]][e[1]]['weight'] = random.randint(1, 8)

	return G


def dijkstraGraph():
	""" 
		Génere une question sur l'algorithme de Dijkstra au format json :
		- question Dijkstra
		- graph pondéré
		- graph dirigé ou non
		- bonne réponse plus court chemin
		- mauvaise réponses

	"""

	avecPoids =  1 # random.randint(0,1) #generation graph pondere
	directed = random.randint(0,1) #aléatoire pour graph dirigé ou non

	question = "{ \"question\": \"D'après l'algorithme de Dijkstra, quel est le plus court chemin entre le noeud A et le noeud E ?\", "

	colorBase = "\"colorbase\": \"{0,4}\", " #noeud a colorer de base

	colorReponse = "\"colorreponse\": " #noeud et edges a colorer a l'affichage de la reponse

	complementReponse = "\"complementreponse\": \"None\", "

	if(avecPoids):
		ponderate = "\"ponderate\": \"True\", "
	else:
		ponderate = "\"ponderate\": \"False\", "


	if(directed):
		base = nx.fast_gnp_random_graph(1,0,None,True) #graph de base pour garder l'attribut directed = true
	else:
		base = nx.fast_gnp_random_graph(1,0,None,False)

	nbrReponse = 0

	while nbrReponse < 2:

		G = nx.path_graph(5,base) #creation path_graph de base à 5 noeuds

		#ajout noeuds supplémentaires
		for i in range(5,10):
			G.add_node(i)

		#ajout random arcs 
		for i in range(0, 10):
			G.add_edge(random.randint(0, 9), random.randint(0, 9))

		#suppression de l'arc A - E si il existe pour compliquer la réponse
		G.add_edge(0,4)
		G.remove_edge(0,4)

		if(avecPoids):
			G = addWeight(G) #ajout des poids random sur les arcs

		nbrReponse = nombreReponse(G)

	G = addEdgesIds(G)
	graph = graphToJson(G) #mise au format Json

	#reponse dijkstra
	true_answer = nx.dijkstra_path(G,0,4,weight="weight")

	reponse_true = ", \"true_answer\": \""

	#change node id to char value + ajout de l'id dans colorreponse
	colorReponse += "{ \"nodes\": \"{"
	for i in true_answer:
		if i == true_answer[len(true_answer)-1]:
			reponse_true += chr(i+65)
			colorReponse += str(i)

		else:

			reponse_true += chr(i+65) +"-"
			colorReponse += str(i) + ", "

	colorReponse += "}\", \"edges\": \"{"

	reponse_true += "\""

	#ajout des arcs à colorer dans colorReponse
	i = 0
	j = 1
	while j < len(true_answer) :
		colorReponse += str(G[true_answer[i]][true_answer[j]]['id']) +","
		i += 1
		j += 1


	colorReponse = colorReponse[:len(colorReponse)-1] #cut dernière virgule
	colorReponse += "}\"}," #fermeture ensemble pour respecter format json
	colorReponse = colorReponse.replace(" ","") #suppression des " " pour un meilleure parsage en javascript

	#mauvaise reponse
	reponse_wrong = ", \"wrong_answer\": \"" + wrongAnswer(G,true_answer) +"\""

	graph = graph[1:len(graph)-1] #cut { et } pour ajouter la question/réponse et garder un format json valide
	graph = question + ponderate + colorBase + colorReponse + complementReponse + str(graph) + str(reponse_true) + reponse_wrong + "}" #ajout question/reponse dans le format json + fermeture de l'objet json avec }

	return graph

def wrongAnswer(graph, arrayTrueAnswer):
	""" Génere des mauvaises réponses pour les algos de Dijkstra et Bellman-Ford """

	wrongAnswer = ""
	compteurWrongAnswer = 0
	allSimplePath = list(nx.all_simple_paths(graph, 0, 4, None)) #tout les chemins de 0 a 4 (A a E)

	i = 0

	while compteurWrongAnswer < 3: #jusqua trouver 3 chemin (3 mauvaises réponses)

		if not compareArray(arrayTrueAnswer, allSimplePath[i]):

			for j in allSimplePath[i]: #transformation id node to lettre
				if j == allSimplePath[i][len(allSimplePath[i])-1]:
					wrongAnswer +=  chr(j+65)
				else:
					wrongAnswer +=  chr(j+65) + "-"

			wrongAnswer += "z"
			compteurWrongAnswer += 1
		i += 1
		if i == len(allSimplePath): #si moins de 3 chemin existant on arrete la boucle
			if(compteurWrongAnswer == 1):
				wrongAnswer += "Utilisation de l'algorithme impossible.z" #si seulement une réponse possible on ajoute cette reponse
				compteurWrongAnswer += 1
			if(compteurWrongAnswer == 2):
				wrongAnswer += "D la réponse D" #si seulement deux réponse on ajoute "D la réponse D"
			compteurWrongAnswer = 3

	return wrongAnswer

def negatifDijkstra():
	""" 
		Génere une question sur l'usage de Dijkstra avec des poids négatifs au format json :
		- question Dijkstra
		- graph pondéré
		- graph dirigé ou non
		- bonne réponse : utilisation de l'algorithme impossible
		- mauvaise réponses

	"""
	question = "{ \"question\": \"D'après l'algorithme de Dijkstra, quel est le plus court chemin entre le noeud A et le noeud E ?\", "
	ponderate = "\"ponderate\": \"True\", "

	colorBase = "\"colorbase\": \"{0,4}\", " #noeud a colorer de base

	colorReponse = "\"colorreponse\": {\"nodes\": \"{"+colorMauvaiseReponse+",0,4}\", \"edges\": \"{"+colorMauvaiseReponse+"," #noeud ou arc a colorer a l'affichage de la reponse

	complementReponse = "\"complementreponse\": \"L'algorithme de Dijkstra ne s'applique pas aux graphes possédant des poids négatifs.\","

	directed = random.randint(0,1) #aléatoire pour graph dirigé ou non

	if(directed):
		base = nx.fast_gnp_random_graph(1,0,None,True) #graph de base pour garder l'attribut directed = true
	else:
		base = nx.fast_gnp_random_graph(1,0,None,False)

	nbrReponse = 0

	while nbrReponse < 3:

		G = nx.path_graph(5,base) #creation path_graph de base à 5 noeuds

		#ajout noeuds supplémentaires
		for i in range(5,10):
			G.add_node(i)

		#ajout random arcs 
		for i in range(0, 10):
			G.add_edge(random.randint(0, 9), random.randint(0, 9))

		#suppression de l'arc A - E si il existe pour compliquer la réponse
		G.add_edge(0,4)
		G.remove_edge(0,4)

		G = addWeightNegatif(G) #ajout des poids random sur les arcs

		nbrReponse = nombreReponse(G)

	G = addEdgesIds(G)
	graph = graphToJson(G) #mise au format Json

		#reponse dijkstra
	true_answer = "Utilisation de l'algorithme impossible."
	reponse_true = ", \"true_answer\": \""


	reponse_true += true_answer +"\""

	#mauvaise reponse
	reponse_wrong = ", \"wrong_answer\": \"" + wrongAnswer(G,true_answer) +"\""

	#coloration arcs négatifs
	for e in G.edges:
		if G.edges[e]['weight'] < 0:
			colorReponse += str(G.edges[e]['id'])+","

	colorReponse += "\"}, "


	graph = graph[1:len(graph)-1] #cut { et } pour ajouter la question/réponse et garder un format json valide
	graph = question + ponderate + colorBase + colorReponse + complementReponse + str(graph) + str(reponse_true) + reponse_wrong + "}" #ajout question/reponse dans le format json + fermeture de l'objet json avec }

	return graph


def addWeightNegatif(G):
	"""  
	Ajoute des poids aléatoire sur les arcs d'un graph G avec au moins un poids négatif
	(le poids négatif obligatoire est ajouté en créant un arc si il n'existe pas)
	
	"""

	source = random.randint(0, 9)
	target = random.randint(0, 9)

	for e in G.edges():
		G[e[0]][e[1]]['weight'] = random.randint(-2, 8)

	G.add_edge(source,target)
	G[source][target]['weight'] = -2

	return G

#question trouver le cardinal de la clique maximale
def cardinalMaxClique():
	""" 
		Génere une question sur le cardinal de la clique maximale d'un graph au format json :
		- question cardinal clique
		- graph non pondéré
		- graph non dirigé
		- bonne réponse cardinal max clique
		- mauvaise réponses

	"""
	question = "{ \"question\": \"Quel est le cardinal de la plus grande clique du graphe ci-dessus ?\", "
	ponderate = "\"ponderate\": \"False\", "

	colorBase = "\"colorbase\": \"None\", " #noeud a colorer de base

	colorReponse = "\"colorreponse\": " #noeud a colorer a l'affichage de la reponse

	complementReponse = "\"complementreponse\": \"None\", "

	nbrReponse = 0

	while nbrReponse < 3:

		G = nx.fast_gnp_random_graph(6,0.7,None,False) #G -> graph non orienté
		colorClique = clique.max_clique(G)
		true_answer = len(colorClique)
		nbrReponse = true_answer

	colorReponse += "{ \"nodes\": \"" + str(colorClique) + "\", \"edges\": \"None\"}, " #recuperation ensemble de noeuds a colorer pour la reponse

	colorReponse = colorReponse.replace(" ","") #suppression des " " pour un meilleure parsage en javascript

	G = addEdgesIds(G)
	graph = graphToJson(G) #mise au format Json

	#reponse card max clique
	reponse_true = ", \"true_answer\": \""
	reponse_true += str(true_answer) +"\""

	#mauvaise reponse
	wa1 = random.randint(1,true_answer-2)
	wa2 = random.randint(true_answer+1, true_answer+4)
	wa3 = random.randint(wa1,wa2)
	while(wa3 == wa1 or wa3 == wa2 or wa3 == true_answer):
		wa1 = random.randint(1,true_answer-2)
		wa2 = random.randint(true_answer+1, true_answer+4)
		wa3 = random.randint(wa1,wa2)

	wrong_answer = str(wa1) + "z" + str(wa2) + "z" + str(wa3) + "z"

	reponse_wrong = ", \"wrong_answer\": \"" + wrong_answer +"\""

	graph = graph[1:len(graph)-1] #cut { et } pour ajouter la question/réponse et garder un format json valide
	graph = question + ponderate + colorBase + colorReponse + complementReponse + str(graph) + str(reponse_true) + reponse_wrong + "}" #ajout question/reponse dans le format json + fermeture de l'objet json avec }

	return graph

def bellmanFord():

	""" 
		Génere une question sur l'agorithme de Dijkstra au format json :
		- question Dijkstra
		- graph pondéré
		- graph dirigé ou non
		- bonne réponse plus court chemin
		- mauvaise réponses

	"""

	avecPoids =  1 # random.randint(0,1) #generation graph pondere

	question = "{ \"question\": \"D'après l'algorithme de Bellman-Ford, quel est le plus court chemin entre le noeud A et le noeud E ?\", "

	if(avecPoids):
		ponderate = "\"ponderate\": \"True\", "
	else:
		ponderate = "\"ponderate\": \"False\", "

	colorBase = "\"colorbase\": \"{0,4}\", " #noeud a colorer de base

	colorReponse = "\"colorreponse\": " #noeud a colorer a l'affichage de la reponse

	complementReponse = "\"complementreponse\": \"None\", "

	base = nx.fast_gnp_random_graph(1,0,None,True) #base -> graph dirigé obligatoire pour utiliser l'ago de bellman-ford
	
	nbrReponse = 0

	while nbrReponse < 3:

		G = nx.path_graph(5,base) #creation path_graph de base à 5 noeuds

		#ajout noeuds supplémentaires
		for i in range(5,10):
			G.add_node(i)

		#ajout random arcs 
		for i in range(0, 10):
			G.add_edge(random.randint(0, 9), random.randint(0, 9))

		#suppression de l'arc A - E si il existe pour compliquer la réponse
		G.add_edge(0,4)
		G.remove_edge(0,4)

		if(avecPoids):
			G = addWeightNegatif(G) #ajout des poids random sur les arcs

		nbrReponse = nombreReponse(G)

	negativeCycle = nx.negative_edge_cycle(G, weight='weight')

	G = addEdgesIds(G)
	graph = graphToJson(G) #mise au format Json

	#si presence de cycle négatif utilisation de bellman-ford impossible
	if(negativeCycle):
		true_answer = "Utilisation de l'algorithme impossible."
		reponse_true = ", \"true_answer\": \""
		reponse_true += true_answer
		colorReponse += "\"None\", "
		complementReponse = "\"complementreponse\": \"L'algorithme de Bellman-Ford ne s'applique pas aux graphes possédant des cycles négatifs.\","

	else:
		true_answer = nx.bellman_ford_path(G, 0, 4, weight='weight')
		reponse_true = ", \"true_answer\": \""

		#change node id to char value
		colorReponse += "{ \"nodes\": \"{"
		for i in true_answer:
			if i == true_answer[len(true_answer)-1]:
				reponse_true += chr(i+65)
				colorReponse += str(i)

			else:

				reponse_true += chr(i+65) +"-"
				colorReponse += str(i) + ", "

		colorReponse += "}\", \"edges\": \"{"

	reponse_true += "\""

	if not negativeCycle :
		#ajout des arcs à colorer dans colorReponse
		i = 0
		j = 1
		while j < len(true_answer) :
			colorReponse += str(G[true_answer[i]][true_answer[j]]['id']) +","
			i += 1
			j += 1


		colorReponse = colorReponse[:len(colorReponse)-1] #cut dernière virgule
		colorReponse += "}\"}," #fermeture ensemble pour respecter format json
		colorReponse = colorReponse.replace(" ","") #suppression des " " pour un meilleure parsage en javascript

	else:
		listCycle = nx.find_cycle(G, source= None, orientation = 'original')
		print(listCycle)
	#mauvaise reponse
	reponse_wrong = ", \"wrong_answer\": \"" + wrongAnswer(G,true_answer) +"\""

	graph = graph[1:len(graph)-1] #cut { et } pour ajouter la question/réponse et garder un format json valide
	graph = question + ponderate + colorBase + colorReponse + complementReponse + str(graph) + str(reponse_true) + reponse_wrong + "}" #ajout question/reponse dans le format json + fermeture de l'objet json avec }

	return graph

def arbreCouvrantMinimal():
	"""
		Génere une question sur les arbres couvrant minimaux au format json :
		- question ACM
		- graph pondéré
		- graph non dirigé
		- bonne réponse ACM
		- mauvaise réponses
	"""

	question = "{ \"question\": \"L'arbre couvrant de poids minimal du graphe ci-dessus est composé des arcs : \", "

	ponderate = "\"ponderate\": \"True\", "

	colorBase = "\"colorbase\": \"None\", " #noeud a colorer de base

	colorReponse = "\"colorreponse\": {\"nodes\" : \"{0,1,2,3,4,5,6,7}\", \"edges\" : \"{" #noeud a colorer a l'affichage de la reponse

	reponse_true = ", \"true_answer\": \""

	complementReponse = "\"complementreponse\": \"None\", "

	connected = 0

	while not connected :

		G = nx.dense_gnm_random_graph(8,12,None)
		connected = nx.is_connected(G)
	
	G = addWeight(G) #ajout des poids random sur les arcs
	G = addLabel(G)

	G = addEdgesIds(G)
	graph = graphToJson(G) #mise au format Json

	true_answer = nx.minimum_spanning_tree(G, weight='weight', algorithm='prim', ignore_nan=True) #generation graph reponse

	for e in sorted(true_answer.edges):	#parcours des arcs du graph reponse
		reponse_true += str(G.edges[e]['label']) + ", " #recuperation des label des arcs dans reponse_true
		colorReponse += str(G.edges[e]['id']) + ","	#recuperation des ids des arcs dans colorReponse

	colorReponse = colorReponse[:len(colorReponse)-1] + "}\"}, "

	reponse_true = reponse_true[:len(reponse_true)-2] #cut dernière virgule + space
	reponse_true += "\", "

	#mauvaise réponse 

	wa1 = ""
	wa2 = ""
	wa3 = ""

	for e in G.edges:
		
		idEdge = G.edges[e]['id']

		#70% de chance d'ajouter un arc du graph à une mauvaise réponse
		if random.randint(0, 9) < 7: 
			wa1 += chr(idEdge + 97) + ", "

		if random.randint(0, 9) < 7:
			wa2 += chr(idEdge + 97) + ", "
		if random.randint(0, 9) < 7:
			wa3 += chr(idEdge + 97) + ", "

	#cut virgule + space
	wa1 = wa1[:len(wa1)-2]
	wa2 = wa1[:len(wa2)-2]
	wa3 = wa1[:len(wa3)-2]
	
	wrong_answer = str(wa1) + "z" + str(wa2) + "z" + str(wa3) + "z"

	reponse_wrong = "\"wrong_answer\": \"" + wrong_answer +"\""

	graph = graph[1:len(graph)-1] #cut { et } pour ajouter la question/réponse et garder un format json valide
	graph = question + ponderate + colorBase + colorReponse + complementReponse + str(graph) + str(reponse_true) + reponse_wrong + "}" #ajout question/reponse dans le format json + fermeture de l'objet json avec }

	return graph

def composanteFortementConnexe():
	"""
		Génere une question sur les composante fortement connexe au format json :
		- question CFC
		- graph non pondéré
		- graph dirigé
		- bonne réponse CFC
		- mauvaise réponses
	"""

	question = "{ \"question\": \"Combien de composantes fortement connexes possède ce graphe ?\", "

	ponderate = "\"ponderate\": \"False\", "

	colorBase = "\"colorbase\": \"None\", " #noeud a colorer de base

	colorReponse = "\"colorreponse\": {\"nodes\": \"{"

	reponse_true = ", \"true_answer\": \""

	complementReponse = "\"complementreponse\": \"None\", "

	G = nx.fast_gnp_random_graph(8,0.15,None,True) #graph dirigé

	true_answer = nx.number_strongly_connected_components(G)	

	reponse_true += str(true_answer)

	reponse_true += "\", "

	G = addEdgesIds(G)
	graph = graphToJson(G) #mise au format Json

	#mauvaise reponse
	wa1 =  random.randint(0,true_answer)
	wa2 = random.randint(true_answer+1, true_answer+3)
	wa3 = random.randint(wa1,wa2)
	while(wa3 == wa1 or wa3 == wa2 or wa3 == true_answer):
		wa1 = random.randint(0,true_answer)
		wa2 = random.randint(true_answer+1, true_answer+3)
		wa3 = random.randint(wa1,wa2)

	wrong_answer = str(wa1) + "z" + str(wa2) + "z" + str(wa3) + "z"


	reponse_wrong = "\"wrong_answer\": \"" + wrong_answer +"\""

	#recuperation cfc pour coloration

	cfc = nx.strongly_connected_components(G)

	i = 0
	for c in cfc:
		colorReponse += listColor[i] + ","
		i += 1
		for d in c:
			colorReponse += str(d) + ","

	colorReponse = colorReponse[:len(colorReponse)-1] +"}\"}, "

	graph = graph[1:len(graph)-1] #cut { et } pour ajouter la question/réponse et garder un format json valide
	graph = question + ponderate + colorBase + colorReponse + complementReponse + str(graph) + str(reponse_true) + reponse_wrong + "}" #ajout question/reponse dans le format json + fermeture de l'objet json avec }

	return graph


def compareArray(array1, array2):
	""" compare deux tableau et rend true si ils sont identiques false sinon """

	if len(array1) != len(array2) :
		return 0

	j = 0
	for i in array1:
		if i != array2[j]:
			return 0
		j+= 1
	return 1

def nombreReponse(graph):
	""" Rend le nombre de chemins possible dans un graph du noeud A(id=0) à E(id=4)"""

	return len(list(nx.all_simple_paths(graph, 0, 4, None)))

def addLabel(G):
	""" prend un graph en paramètre ajoute un label sur ces arcs arc(0) -> label = a etc... """
	i = 0
	for e in G.edges():
		G[e[0]][e[1]]['label'] = chr(i+97)
		i += 1

	return G

def addEdgesIds(G):
	""" prend un graph en paramètre ajoute un id sur ces arcs allant de 0 au nombre d'arcs """
	i = 0
	for e in G.edges():
		G[e[0]][e[1]]['id'] = i
		i += 1

	return G