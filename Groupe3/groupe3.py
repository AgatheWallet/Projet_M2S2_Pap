#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Avec un fichier long, comme dans notre corpus, vous finirez par avoir des soucis d'erreurs de récursions.
Il y a deux manières de résoudre ce problème:
- augmenter la limite de recursion avec le module sys (à vos risques et périls...),
- transformer le code pour passer d'un code récursif à un code itératif (ce qui n'est pas le but de ce projet).

Le formatage des résultats a été discuté avec et approuvé par le groupe 5.

Le fichier peut-être appelé de cette manière dans le terminal
	$ python groupe3.py [chemin/vers/dossier_corpus/]
"""

import sys
sys.setrecursionlimit(6000)
import time
import re
import spacy
from spacy.tokens.doc import Doc
nlp = spacy.load("fr_core_news_sm")
import json
from glob import glob
import matplotlib.pyplot as plt


def preprocess_file(inputFile: str, cpt_temps: int, cpt_espace: int) -> tuple:
	""" ouvre le fichier texte, le découpe au niveau des '\n', le nettoie 
 	et appelle la fonction analyse_spacy() pour analyser le texte

	Args:
		inputFile (str): chemin vers le fichier
		cpt_temps (int): compteur pour la complexité en temps
		cpt_espace (int): compteur pour la complexité en espace

	Returns:
		tuple: un dico de dicos où chaque dico correspond à une phrase analysée,
  		les compteurs de temps et d'espace
	"""
	with open(inputFile, 'r') as file:
		texte = [line.rstrip() for line in file.readlines()]
		texte = [re.sub(r"^ +", "", line) for line in texte]
		texte = [re.sub(r" +", " ", line) for line in texte if line != ""]
		if len(texte) == 0:
			return [], cpt_temps, cpt_espace
		# 'textes' est une liste de lignes présentes
		# jusqu'à la fin de l'exécution du programme 
		# on l'ajoute donc à notre compteur
		cpt_espace = len(texte)
		return analyse_spacy(texte, cpt_temps+1, cpt_espace)


def analyse_spacy(texte: list[str], cpt_temps: int, cpt_espace: int) -> tuple:
	""" analyse le texte avec spacy

	Args:
		texte (list[str]): liste de phrase
		cpt_temps (int): compteur pour la complexité en temps
		cpt_espace (int): compteur pour la complexité en espace
		
	Returns:
		tuple: un dico de dicos où chaque dico correspond à une phrase analysée,
  		les compteurs de temps et d'espace
	"""
	docs = list(nlp.pipe(texte, disable=["parser", "lemmatizer", "attribute_ruler"]))
	# 'docs' contient le texte analysé par spacy, on rajoute le nombre d'élément dans la variable 'cpt_espace'
	# on ne calcule pas seulement le nombre d'élément dans docs, mais le nombre d'éléments dans chaque élément de docs
	cpt_espace += sum([len(doc) for doc in docs])
	# le nombre de tokens selon la tokenisation de spacy
	nb_tokens = sum([len(doc) for doc in docs])
	return process_file([], docs, cpt_temps+1, cpt_espace), nb_tokens


def process_file(dicos: list[dict], docs: list[Doc], cpt_temps: int, cpt_espace: int) -> tuple:
	""" traite le texte analysé par spacy ligne par ligne pour créer
	un dico avec comme clé l'index de la phrase et comme valeurs le dico
	contenant les tokens

	Args:
		dicos (list[dict]): chaque dico correspond à une phrase analysé
		docs (list[Doc]): liste de phrase analysé avec spacy
		cpt_temps (int): compteur pour la complexité en temps
		cpt_espace (int): compteur pour la complexité en espace

	Returns:
		tuple: un dico de dicos où chaque dico correspond à une phrase analysée,
  		les compteurs de temps et d'espace
	"""
	# lorsqu'une nouvelle phrase analysée apparaît dans la liste 'dicos'
	# elle est supprimée de la liste 'docs' à la ligne d'après
	# donc on doit calculer si à la ligne 72, cpt_espace est plus grand ou plus petit 
	if len(docs) == 0:
		return dicos, cpt_temps, cpt_espace
	else:
		dicos.append({})
		dicos, cpt_temps, cpt_espace = process_line(0, dicos, docs[0], cpt_temps+1, cpt_espace)
		# 'cpt_def' correspond à len(textes)+len(docs)+len(dicos)
		cpt_def = (len(dicos)+len(docs)-1)+sum([len(doc) for doc in docs])+sum([1 for dico in dicos for token in dico.keys()])
		if cpt_def > cpt_espace:
			cpt_espace = cpt_def
		return process_file(dicos, docs[1:], cpt_temps+1, cpt_espace)


def process_line(i: int, dicos: list[dict], doc: Doc, cpt_temps: int, cpt_espace: int) -> tuple:
	""" traite la ligne analysé par spacy pour créer un dico avec comme clé l'index
	du token et comme valeur un dictionnaire avec deux clé, la forme du token et 
	son annotation en entité nommé

	Args:
		i (int): l'index du token à analyser
		dicos (dict): chaque dico correspond à une phrase analysé
		doc (Doc): la ligne analysé par spacy
		cpt_temps (int): compteur pour la complexité en temps
		cpt_espace (int): compteur pour la complexité en espace

	Returns:
		tuple: un dico de dicos où chaque dico correspond à une phrase analysée,
  		les compteurs de temps et d'espace
	"""
	# nous ne calculons pas l'espace mémoire ici 
	# nous le calculons dans la ligne après l'appel de cette fonction
	if len(doc) == 0:
		return dicos, cpt_temps, cpt_espace
	else:
		if doc[0].ent_iob_ != "O":
			dicos[-1][f"token_{i}"] = { "form": doc[0].text, "ner": doc[0].ent_iob_+"-"+doc[0].ent_type_}
		else:
			dicos[-1][f"token_{i}"] = { "form": doc[0].text, "ner": "O"}
		return process_line(i+1, dicos, doc[1:], cpt_temps+1, cpt_espace)


def get_complexities(chemin: str) -> list:
	""" Cette fonction permet d'obtenir les complexités pour chacun des fichiers.
	Il renvoie une 
    
	Args:
		chemin (str): chemin vers le dossier du corpus
  
	Returns:
		list: liste de quatre listes pour les tokens, la complexité en temps avec time, 
		la complexité en espace, et la complexité en temps avec le compteur d'appel de fonctions.
	"""
	complexities = [[], [], [], []]
	for file in glob(f"{chemin}*.txt"):
		
		start_time = time.time() # début du calcul du temps d'exécution
		(dicos, temps, espace), nb_tokens = preprocess_file(file, cpt_temps=1, cpt_espace=0) # on commence ce compteur temps à 1 car la fonction est appelée
		end_time = time.time() # fin du calcul du temps d'exécution

		complexities[0].append(nb_tokens)
		complexities[1].append(round(end_time - start_time, 3))
		complexities[2].append(espace)
		complexities[3].append(temps)

		print("\nPour le fichier", file, ":")
		print("Les fonctions ont été appelées", temps, "fois.")
		print("Les fonctions auront tourné", round(end_time - start_time, 3), "secondes.")
		print("Dans l'espace mémoire, il y a eu au maximum", espace, "éléments à un moment T.")
		print("Ce fichier fait", nb_tokens, "tokens.")
		
	return complexities


def get_annotations(chemin: str) -> dict:
	""" Cette fonction renvoie un dictionnaire contenant
	tous les textes annotées
 
	Args:
		chemin (str): chemin vers le dossier du corpus
  
	Returns:
		dict: renvoie LE dictionnaire des entitées nommées

 	"""
	# on crée un
	all_dicos = {}
	for file in glob(f"{chemin}*.txt"):
		(dicos, temps, espace), nb_tokens = preprocess_file(file, cpt_temps=1, cpt_espace=0)
		all_dicos[file] = {}
		for i, dico in enumerate(dicos):
			all_dicos[file]["phrase_"+str(i)] = dico
  
	return all_dicos


def make_plot(liste_res:list):

	# Préparation des données de axe x : tri par rapport au nbre de tokens
	combined = list(zip(liste_res[0], liste_res[1], liste_res[2], liste_res[3]))
	sorted_on_ntokens = sorted(combined, key=lambda x: x[0])
	nb_toks, temps, espace, appels = zip(*sorted_on_ntokens)

	# Création de la première figure et de l'axe principal
	# espace x temps (avec module time)
	fig, ax1 = plt.subplots()
	
	# Axe des x et premier axe y (temps)
	ax1.set_xlabel('Nombre de tokens')
	ax1.set_ylabel('Temps (s)', color='green')
	ax1.plot(nb_toks, temps, color='green', marker='o', label='Temps (s)')
	ax1.tick_params(axis='y', labelcolor='green')

	#Création d'un second axe y (espace)
	ax2 = ax1.twinx()
	ax2.set_ylabel('Espace mémoire (unités)', color='purple')
	ax2.plot(nb_toks, espace, color='purple', marker='o', linestyle='-', label='Espace mémoire (unités)')
	ax2.tick_params(axis='y', labelcolor='purple')
 
	# Titre et légendes
	fig.tight_layout() # Ajuste la mise en page pour éviter les chevauchements
	plt.title('Complexité en temps(s) et espace selon le nombre de tokens')

	# Affichage
	plt.grid()
	plt.subplots_adjust(top=0.9)  # Ajuster pour donner plus d'espace au titre
	plt.savefig("plot_temps_espace.png", bbox_inches='tight')
	plt.show()

	# Création de la figure et de l'axe principal
 	# espace x temps (en calculant le nombre d'appels pendant l'execution)
	fig, ax1 = plt.subplots()
	
	# Axe des x et premier axe y (temps)
	ax1.set_xlabel('Nombre de tokens')
	ax1.set_ylabel('Nbre appels fonctions', color='blue')
	ax1.plot(nb_toks, appels, color='blue', marker='o', label='Nbre appels fonctions')
	ax1.tick_params(axis='y', labelcolor='blue')

	#Création d'un second axe y (espace)
	ax2 = ax1.twinx()
	ax2.set_ylabel('Espace mémoire (unités)', color='purple')
	ax2.plot(nb_toks, espace, color='purple', marker='o', linestyle='-', label='Espace mémoire (unités)')
	ax2.tick_params(axis='y', labelcolor='purple')

	# Titre et légendes
	fig.tight_layout() # Ajuste la mise en page évite les chevauchements
	plt.title('Complexité en temps(appels) et espace selon le nombre de tokens')
	# Affichage
	plt.grid()
	plt.subplots_adjust(top=0.9)
	plt.savefig("plot_appels_espace.png", bbox_inches='tight')
	plt.show()


if __name__ == "__main__":

	# on obtient les compteurs et on les affiche dans deux graphiques
	complex = get_complexities(sys.argv[1])
	make_plot(complex)
	
	LE_dico = get_annotations(sys.argv[1])
	# enregistre dans un fichier json nos annotations
	with open('annotations_EN.json', 'w', encoding='utf-8') as file:
		json.dump(LE_dico, file, ensure_ascii=False, indent=4)