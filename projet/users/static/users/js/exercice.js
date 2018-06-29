/**
*	@file
*	Affiche un exercice concernant le cours Algorithmique des graphes
*
*/

var jsonData;

var typePrecedent = "random";

//couleur utiliser pour la coloration des réponses
var colorDefault = "yellow";


$(document).ready(runScript());


/**
*	@function	runScript(typeExercice)
*	Effectue une requete ajax au serveur pour demander un exercice,
*	puis affiche le graph et met à jour le qcm de la page
*	
*	@param {String} typeExercice - le type d'exercice demandé :
*		- "diskstra", "bellmanford", "clique", "acm", "cfc", "random"
*		par defaut "random" ou le type d'exercice précédent
*/
function runScript(typeExercice = typePrecedent){
	$.get({
            url: "http://127.0.0.1:8000/graph",
            data: {
            	'typeExercice': typeExercice
            },
            dataType : 'html',
            success: function(data, statut) {
              	
            	//alert(data);

            	typePrecedent = typeExercice;

                jsonData = data;

				var objJson = JSON.parse(jsonData);

				var data = genererData(objJson);

				affichGraph1(data,objJson);

				//affichage question/réponse
				afficheQuestionReponse(objJson);
            },

            error: function(data, statut, erreur) {

                alert("error");
                //alert(data);

            },

            });
}

/**
*	@function	parseGraphDataNode(graphData)
*	Parse le json reçu en paramètre et en extrait les noeuds du graphes pour créer un DataSet les contenant.
*
*	@param {JSON}	graphData - le json de l'exercice envoyé par le serveur
*	@return {DataSet}	nodes - un DataSet contenant les noeuds du graphs
*
*/
function parseGraphDataNode(graphData){
	var nodes = new vis.DataSet();

	var array = graphData.nodes;

	for(var i = 0 ; i < array.length ; i++){

		nodes.add({id: array[i].id, label: String.fromCharCode(65 + array[i].id)}); //add dans le dataset node

	}

	return nodes;
}

/**
*	@function	parseGraphDataEdge(graphData)
*	Parse le json reçu en paramètre et en extrait les arcs du graphes pour créer un DataSet les contenant en conservant leurs id/label/weight.
*
*	@param {JSON}	graphData - le json de l'exercice envoyé par le serveur
*	@return {DataSet}	nodes - un DataSet contenant les arcs du graphs en conservant leurs id/label/weight
*
*/
function parseGraphDataEdge(graphData){
	var edges = new vis.DataSet();

	var array = graphData.links;

	if(graphData.ponderate == "True"){
		for(var i = 0; i < array.length ; i++){

			if((typeof array[i].label) == "undefined"){
				edges.add({id: array[i].id , from: array[i].source , to : array[i].target , label: array[i].weight.toString()});
			}else{
				edges.add({id: array[i].id ,from: array[i].source , to : array[i].target , label: (array[i].label.toString() + ":" + array[i].weight.toString())});
			}
		

		}
	}else{
		for(var i = 0; i < array.length ; i++){

		edges.add({from: array[i].source , to : array[i].target });

	}
	}
	

	return edges;
}

/**
*	@function	affichGraph1(data, jsonData)
*	Affiche le graph dans le container "graphe" de la page
*
*	@param {Set(DataSet)}	data - un set contenant deux DataSet, un pour les noeuds et un pour les arcs
*	@param {JSON}	jsonData - le json de l'exercice envoyé par le serveur
*
*/
function affichGraph1(data, jsonData){


	if(typeof jsonData.colorbase != "undefined" && jsonData.colorbase != "None"){
		updateNodeColor(data, jsonData.colorbase);
	}
	

	var container = document.getElementById('graphe');

	var options = setOption(jsonData);


    // initialize your network!
    var network = new vis.Network(container, data, options);

}

/**
*	@function	genererData(objJson)
*	Parse les données de l'exercice à l'aide des fonctions parseGraphDataNode et parseGraphDataEdge et crée un set contenant les données
*	renvoyé par ses fonctions.
*
*	@param {JSON}	jsonData - le json de l'exercice envoyé par le serveur
*
*	@return {Set(DataSet)}	data - un set contenant deux DataSet, un pour les noeuds et un pour les arcs
*/
function genererData(objJson){
	var parseNode = parseGraphDataNode(objJson);
	var parseEdge = parseGraphDataEdge(objJson);
	
	var data = {
	nodes: parseNode,
	edges: parseEdge
	};

	return data;

}

/**
*	@function	updateNodeColor(data, newColor)
*	Met à jour la couleur des noeuds du graphs en fonctions des infos apporté par le param newColor
*
*	@param {set(DataSet)}	data - un set contenant deux DataSet, un pour les noeuds et un pour les arcs
*	@param {String} 	newColor - String de la forme "{y1,x1,x2,y2,x3,...}" x = l'id des noeuds a colorer, 
*								y = une couleur pour colorer les prochains noeuds spécifiquement
*								(ici x1 et x2 seront colorer de la couleur y1 et x3 de la couleur y2)
*
*	@return {Set(DataSet)}	data - un set contenant deux DataSet, un pour les noeuds (dont la couleur à été modifié) et un pour les arcs
*/
function updateNodeColor(data, newColor){
	var arrayNodes = data.nodes.getIds();
	var color = colorDefault;

	newColor = newColor.replace(" ","");
	//transformation string to array
	newColor = newColor.split("{");
	newColor = newColor[1].split("}");
	newColor = newColor[0].split(",");

	for(var i = 0 ; i < newColor.length ; i++){
			
		if(contains(arrayNodes, newColor[i])){
			
			data.nodes.update({id: newColor[i], color:{background : color}});

		}else{ //recupération d'une couleur spécifique fournis par le serveur

			color = newColor[i];

		}
		
	} 

	return data;
}

/**
*	@function	updateEdgeColor(data, newColor)
*	Met à jour la couleur des arcs du graphs en fonctions des infos apporté par le param newColor
*
*	@param {set(DataSet)}	data - un set contenant deux DataSet, un pour les noeuds et un pour les arcs
*	@param {String} 	newColor - String de la forme "{y1,x1,x2,y2,x3,...}" x = l'id des arcs a colorer, 
*								y = une couleur pour colorer les prochains arcs spécifiquement
*								(ici x1 et x2 seront colorer de la couleur y1 et x3 de la couleur y2)
*
*	@return {Set(DataSet)}	data - un set contenant deux DataSet, un pour les noeuds et un pour les arcs (dont la couleur à été modifié).
*/
function updateEdgeColor(data, newColor){
	var arrayEdges = data.edges.getIds();
	var color = colorDefault;
	
	newColor = newColor.replace(" ","");
	//transformation string to array
	newColor = newColor.split("{");
	newColor = newColor[1].split("}");
	newColor = newColor[0].split(",");

	for(var i = 0 ; i < newColor.length ; i++){
			
		if(contains(arrayEdges, newColor[i])){

			data.edges.update({id: newColor[i], color:{color : color}});

		}else{ //recupération d'une couleur spécifique fournis par le serveur
		
			color = newColor[i];

		}
		
	} 

	return data;
}

/**
*	@function	setOption(dataJson)
*	Génere les options vis pour l'affichage du graph :
*	affichage des flèches au bout des arcs si le graphe est dirigé
*	+ toute les autres options esthétiques
*
*	@param {JSON}	jsonData - le json de l'exercice envoyé par le serveur
*
*	@return {Set()}	options - un set contenant les options du graphe pour que vis le génère.
*/
function setOption(dataJson){
	var option = {};

	if(dataJson.directed == "True"){
		
		options = {
        autoResize: true,
        height: '100%',
        width: '100%',
        /*configure: {
            showButton: false
        },*/
        edges: {arrows:"to"},
		};
	}else{
		options = {
        autoResize: true,
        height: '100%',
        width: '100%',
        /*configure: {
            showButton: false
        },*/
		}
	}

	return options
}

/**
*	@function	afficheQuestionReponse(jsonData)
*	Affiche la question et les réponses (provenant de l'exercice envoyé par le serveur) dans la page Html au emplacement prévue.
*
*	@param {JSON}	jsonData - le json de l'exercice envoyé par le serveur
*
*/
function afficheQuestionReponse(jsonData){
	
	document.getElementById("question").innerHTML = jsonData.question; //recup question

	//bonne reponse = jsonData.true_answer

	var jsonMauvaiseReponse = jsonData.wrong_answer.toString(); //recup mauvaise reponse

	var mauvaiseReponse = jsonMauvaiseReponse.split("z");

	if(mauvaiseReponse.length == 3){
		
		var arrayRandom = new Array(jsonData.true_answer, mauvaiseReponse[0], mauvaiseReponse[1]);

		document.getElementById("choix4S").innerHTML = mauvaiseReponse[2];

		arrayRandom = shuffle(arrayRandom);

		document.getElementById("choix1S").innerHTML = arrayRandom[0];

		document.getElementById("choix2S").innerHTML = arrayRandom[1];

		document.getElementById("choix3S").innerHTML = arrayRandom[2];

		

	}else{

		var arrayRandom = new Array(jsonData.true_answer, mauvaiseReponse[0], mauvaiseReponse[1], mauvaiseReponse[2]);

		arrayRandom = shuffle(arrayRandom);

		document.getElementById("choix1S").innerHTML = arrayRandom[0];

		document.getElementById("choix2S").innerHTML = arrayRandom[1];

		document.getElementById("choix3S").innerHTML = arrayRandom[2];

		document.getElementById("choix4S").innerHTML = arrayRandom[3];


	}
	

	
}

/**
*	@function shuffle(a)
*	Melange un tableau d'élément
*
*	@param {Array}	a - un tableau d'élément
*
*	@return {Array} a - le tableau passé en paramètre mélangé.
*/
function shuffle(a)
{
   var j = 0;
   var valI = '';
   var valJ = valI;
   var l = a.length - 1;
   while(l > -1)
   {
		j = Math.floor(Math.random() * l);
		valI = a[l];
		valJ = a[j];
		a[l] = valJ;
		a[j] = valI;
		l = l - 1;
	}
	return a;
 }

/**
*	@function	affichGraph2(data, jsonData)
*	Colore les noeuds et arcs de la réponse et affiche le graph dans le container "graphe" de la page
*
*	@param {Set(DataSet)}	data - un set contenant deux DataSet, un pour les noeuds et un pour les arcs
*	@param {JSON}	jsonData - le json de l'exercice envoyé par le serveur
*
*/
function afficherGraph2(data, jsonData){
	var colorReponse ;

	if (typeof jsonData.colorreponse != "undefined" && jsonData.colorreponse != "None"){ //si il y a une réponse a colorer

		colorReponse = jsonData.colorreponse;

		if(typeof colorReponse.nodes != "undefined" && colorReponse.nodes != "None"){ //si il y a des noeuds à colorer

			updateNodeColor(data, colorReponse.nodes);
		}

		if(typeof colorReponse.edges != "undefined" && colorReponse.edges != "None"){ //si il y a des arcs à colorer
		
			updateEdgeColor(data, colorReponse.edges);
		}
	}
	

	var container = document.getElementById('graphe');

	var options = setOption(jsonData);


    // initialize your network!
    var network = new vis.Network(container, data, options);
}

/**
*	@function	reponse()
*	Vérifie si l'utilisateur à entré la bonne réponse, si oui affiche une alert "Bonne réponse ! + (complément réponse si il existe)", 
*	si il y a une erreur affiche une alert "Mauvaise réponse."
*
*/
 function reponse(){

	var objJson = JSON.parse(jsonData);
	var data = genererData(objJson);

 	var choix1 = document.getElementById("choix1").checked;
 	var choix2 = document.getElementById("choix2").checked;
 	var choix3 = document.getElementById("choix3").checked;
 	var choix4 = document.getElementById("choix4").checked;

 	choix = choix1 + choix2 + choix3 + choix4; 

 	switch(choix){
 		case 0 : {
 			alert("Veuillez cocher une réponse.");
 		}break;
 		case 1 : {
 			if(choix1){
 				if(document.getElementById("choix1S").innerHTML == objJson.true_answer){
 					 bonneReponse(objJson);

					afficherGraph2(data, objJson);
 				}else{
 					alert("Mauvaise réponse.");
 				}
 			}else if(choix2){
 				if(document.getElementById("choix2S").innerHTML == objJson.true_answer){
 					bonneReponse(objJson);

					afficherGraph2(data, objJson);
 				}else{
 					alert("Mauvaise réponse.");
 				}
 			}else if(choix3){
 				if(document.getElementById("choix3S").innerHTML == objJson.true_answer){
 					bonneReponse(objJson);

					afficherGraph2(data, objJson);
 				}else{
 					alert("Mauvaise réponse.");
 				}
 		}else if(choix4){
 				if(document.getElementById("choix4S").innerHTML == objJson.true_answer){
 					bonneReponse(objJson);

					afficherGraph2(data, objJson);
 				}else{
 					alert("Mauvaise réponse.");
 				}
 		}
 	}break;
 	default: alert("Une seule réponse possible.");
 }
}

/**
*	@function	bonneReponse(dataJson)
*	Affiche une alert "Bonne réponse ! + (complément réponse si il existe dans les données de l'exercice envoyé par le serveur)" 
*
*/
function bonneReponse(dataJson){
	if(dataJson.complementreponse != undefined && dataJson.complementreponse  != "None"){

		alert("Bonne réponse !\n"+dataJson.complementreponse);

	}else{
		alert("Bonne réponse !");
	}
}

/**
*	@function	contains(array, element)
*	Custom contains pour vérifier si un élément est présent dans un tableau
*
*	@param {Array(element)}	array - un tableau
*	@param {element}	element - un element
*
*	@return {boolean}	True si element se trouve dans array, False sinon.
*
*/
function contains(array, element) {
    for (var i = 0; i < array.length; i++) {
    	
        if (parseInt(array[i]) == parseInt(element)) {
            return true;
        }
    }
    return false;
}