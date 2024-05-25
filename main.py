#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pour exécuter ce script : 
$ python3 groupe5.py chemin/du/corpus chemin/du/fichier/output

"""
"""
Pour exécuter ce script :
\$ python3 main.py chemin/du/corpus chemin/du/fichier/output.conllu

Ce script est conçu pour traiter un corpus de texte et générer un fichier de sortie au format CoNLL.
Il utilise les scripts des groupes 1 à 4 pour effectuer différentes tâches de traitement automatique des langues.

Les étapes principales sont les suivantes :
1. Prétraitement du corpus (groupe 1 : Sandra JAGODZINSKA et Valentina OSETROV)
2. Analyse syntaxique et sémantique (groupe 2 : Kenza AHMIA, Liza FRETEL et Shami THIRION SEN)
3. Reconnaissance des entités nommées (groupe 3 : Laura DARENNE et Alice WALLARD)
4. Analyse des groupes nominaux (groupe 4 : Fanny BACHEY, Clément BUON et Tifanny NGUYEN)
5. Génération du fichier de sortie au format CoNLL (groupe 5 : Florian Jacquot et Agathe WALLET)
"""

import sys
import spacy.tokens
from glob import glob
from pprint import pprint
from collections import defaultdict
import spacy
import numpy as np
import matplotlib.pyplot as plt
import math
import io

from Groupe1.groupe1 import process_gp1, recursive_tokens_pos
from Groupe1.groupe1 import get_complexity_time as g1_get_complexity_time
from Groupe1.groupe1 import get_complexity_space as g1_get_complexity_space

from Groupe2.groupe2 import process_gp2
from Groupe2.groupe2 import n_tokens as g2_n_tokens
from Groupe2.groupe2 import time_data as g2_time_data
from Groupe2.groupe2 import memory_data as g2_memory_data

from Groupe3.groupe3 import get_annotations as process_gp3
from Groupe3.groupe3 import get_complexities as g3_get_complexities

from Groupe4.groupe4 import process_gp4

print("Début du programme, fin des affichages...")

# pour supprimer tous les affichages ralentissant l'exécution
sys_stdout = sys.stdout 
sys.stdout = io.StringIO()


def pretraitement_dico_gn(dico_gp4: dict) -> dict:
	"""
	Cette fonction prend en entrée un dictionnaire contenant les résultats de l'analyse des groupes nominaux (groupe 4) et renvoie un nouveau dictionnaire avec une structure plus adaptée pour la suite du traitement.

	Args:
	- dico_gp4 (dict) : dictionnaire contenant les résultats de l'analyse des groupes nominaux

	Returns:
	- new_dict (dict) : nouveau dictionnaire avec une structure plus adaptée pour la suite du traitement
	"""
	new_dict = {}
	dico_gp4 = [dico_phrase for dico_phrase in dico_gp4 if len(dico_phrase) > 0 or (len(dico_phrase) == 1 and dico_phrase[0][0].text.strip() != "") ]
	compteur_phrase = 0
	for subdict in dico_gp4:
		new_dict.update({f"phrase_{compteur_phrase}":{}})
		tok_compteur = 0
		for i in range(len(subdict)):
			form = subdict[i][0].text
			if form.strip() != "":
				new_dict[f"phrase_{compteur_phrase}"].update({f"token_{tok_compteur}": {"form": form, "noun_phrase": subdict[i][1]}})
				tok_compteur +=1
		compteur_phrase +=1
	return new_dict




def analyse_line(line_doc: spacy.tokens.doc.Doc, dico_phrase : dict, dico_named_entites: dict, dico_noun_phrases: dict ):
	"""
	Cette fonction prend en entrée un objet Doc de spaCy représentant une ligne de texte,
	ainsi que trois dictionnaires contenant les résultats des analyses précédentes,
	et renvoie un dictionnaire contenant les résultats de l'analyse de la ligne de texte.

	Args:
	- line_doc (spacy.tokens.doc.Doc) : objet Doc de spaCy représentant une ligne de texte
	- dico_phrase (dict) : dictionnaire contant les résultats de l'analyse de la ligne de texte (initialement vide)
	- dico_named_entites (dict) : dictionnaire contenant les résultats de la reconnaissance des entités nommées (groupe 3)
	- dico_noun_phrases (dict) : dictionnaire contenant les résultats de l'analyse des groupes nominaux (groupe 4)
	
	Returns:
	- dico_phrase (dict) : dictionnaire contenant les résultats de l'analyse de la ligne de texte
	"""
	for sent in line_doc:
		liste_token = [token for token in sent]
		return get_pos(liste_token, 0, dico_phrase, dico_named_entites, dico_noun_phrases)
		

def get_pos(liste_token: list, tok_id: int, dico_phrase: dict, dico_named_entites: dict, dico_noun_phrases: dict):
	"""
	Cette fonction prend en entrée une liste de tokens, un identifiant de token, ainsi que trois dictionnaires contenant les résultats des analyses précédentes, et renvoie un dictionnaire contenant les résultats de l'analyse du token.
	
	Args:
	- liste_token (list) : liste de tokens
	- tok_id (int) : identifiant de token
	- dico_phrase (dict) : dictionnaire contenant les résultats de l'analyse de la ligne de texte
	- dico_named_entites (dict) : dictionnaire contenant les résultats de la reconnaissance des entités nommées (groupe 3)
	- dico_noun_phrases (dict) : dictionnaire contenant les résultats de l'analyse des groupes nominaux (groupe 4)
	
	Returns:
	- dico_phrase (dict) : dictionnaire contenant les résultats de l'analyse de la ligne de texte
	"""
	if tok_id < len(liste_token):
		token = liste_token[tok_id]
		dico_phrase.update({f"token_{tok_id}":{"form":token.text, "pos":token.pos_}})
		return get_dep(liste_token, tok_id, dico_phrase, dico_named_entites, dico_noun_phrases)
	
	else:
		return dico_phrase
	
def get_dep(liste_token: list, tok_id: int, dico_phrase: dict, dico_named_entites: dict, dico_noun_phrases: dict):
	"""
	Cette fonction prend en entrée une liste de tokens, un identifiant de token, ainsi que trois dictionnaires contenant les résultats des analyses précédentes, et renvoie un dictionnaire contenant les résultats de l'analyse du token.
	
	Args:
	- liste_token (list) : liste de tokens
	- tok_id (int) : identifiant de token
	- dico_phrase (dict) : dictionnaire contenant les résultats de l'analyse de la ligne de texte
	- dico_named_entites (dict) : dictionnaire contenant les résultats de la reconnaissance des entités nommées (groupe 3)
	- dico_noun_phrases (dict) : dictionnaire contenant les résultats de l'analyse des groupes nominaux (groupe 4)

	Returns:
	- dico_phrase (dict) : dictionnaire contenant les résultats de l'analyse de la ligne de texte
	"""
	token = liste_token[tok_id]
	dico_phrase[f"token_{tok_id}"].update({"dep": token.dep_, "head": token.head})
	return get_ne(liste_token, tok_id, dico_phrase, dico_named_entites, dico_noun_phrases)


def get_ne(liste_token, tok_id: int, dico_phrase: dict, dico_named_entites: dict, dico_noun_phrases: dict):
	"""
	Cette fonction prend en entrée une liste de tokens, un identifiant de token, ainsi que trois dictionnaires contenant les résultats des analyses précédentes, et renvoie un dictionnaire contenant les résultats de l'analyse du token.

	Args:
	- liste_token (list) : liste de tokens
	- tok_id (int) : identifiant de token
	- dico_phrase (dict) : dictionnaire contenant les résultats de l'analyse de la ligne de texte
	- dico_named_entites (dict) : dictionnaire contenant les résultats de la reconnaissance des entités nommées (groupe 3)
	- dico_noun_phrases (dict) : dictionnaire contenant les résultats de l'analyse des groupes nominaux (groupe 4)

	Returns:
	- dico_phrase (dict) : dictionnaire contenant les résultats de l'analyse de la ligne de texte
	"""
	if dico_phrase[f"token_{tok_id}"]["form"] == dico_named_entites[f"token_{tok_id}"]["form"]:
		dico_phrase[f"token_{tok_id}"].update({"named_entites" : dico_named_entites[f"token_{tok_id}"]["ner"]})
		return get_np(liste_token, tok_id, dico_phrase, dico_named_entites, dico_noun_phrases)
	else:
		print(tok_id)
		print(dico_phrase[f"token_{tok_id}"])
		print(dico_named_entites[f"token_{tok_id}"])
		print("erreur !")

def get_np(liste_token, tok_id: int, dico_phrase:dict, dico_named_entites: dict, dico_noun_phrases: dict):
	"""
	Cette fonction prend en entrée une liste de tokens, un identifiant de token,
	ainsi que trois dictionnaires contenant les résultats des analyses précédentes,
	et renvoie un dictionnaire contenant les résultats de l'analyse du token.

	Args:
	- liste_token (list) : liste de tokens
	- tok_id (int) : identifiant de token
	- dico_phrase (dict) : dictionnaire contenant les résultats de l'analyse de la ligne de texte
	- dico_named_entites (dict) : dictionnaire contenant les résultats de la reconnaissance des entités nommées (groupe 3)
	- dico_noun_phrases (dict) : dictionnaire contenant les résultats de l'analyse des groupes nominaux (groupe 4)

	Returns:
	- dico_phrase (dict) : dictionnaire contenant les résultats de l'analyse de la ligne de texte
	"""
	if dico_noun_phrases[f"token_{tok_id}"]["form"] == dico_phrase[f"token_{tok_id}"]["form"]:
		dico_phrase[f"token_{tok_id}"].update({"noun_phrase":dico_noun_phrases[f"token_{tok_id}"]["noun_phrase"]})
		return get_pos(liste_token, tok_id + 1, dico_phrase, dico_named_entites, dico_noun_phrases)
	else:
		print(dico_phrase[f"token_{tok_id}"]["form"])
		print(dico_noun_phrases[f"token_{tok_id}"]["form"])
		print("erreur !!")


def build_dico(corpus_path):
	"""
	Cette fonction prend en entrée le chemin d'accès à un corpus de texte et renvoie un dictionnaire
	contenant les résultats de l'analyse du corpus.

	Args:
	- corpus_path (str) : chemin d'accès à un corpus de texte

	Returns:
	- dico (dict) : dictionnaire contenant les résultats de l'analyse du corpus
	"""
	dico = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
	dico_ne = process_gp3(corpus_path)
	cpxs_gp1 = [[], []] # time, space
	cpxs_gp2 = [[], [], []] # nb_tokens, time, space
	cpxs_gp3 = g3_get_complexities(corpus_path)
	cpxs_gp4 = []
	for file in glob(f"{corpus_path}*.txt"):
		c_time = g1_get_complexity_time(file)
		c_space = g1_get_complexity_space()
		cpxs_gp1[0].append(c_time)
		cpxs_gp1[1].append(c_space)
		with open(file) as rf:
			dico_gn, cpx_gp4 = process_gp4(file)
			cpxs_gp4.append(cpx_gp4)
			dico_gn = pretraitement_dico_gn(dico_gn)
			# pprint(dico_gn)
			compteur_phrases = 0
			for line in rf : 
				# print(compteur_phrases)
				line = line.strip()
				if line!= "":
					dico[file.split('/')[-1]][f"phrase_{compteur_phrases}"]["text"] = line
					# print((dico_ne[file][f"phrase_{compteur_phrases}"]))
					print(file)
					sent_doc = process_gp2(process_gp1([line]))
					for sent in sent_doc:
						dico[file.split('/')[-1]][f"phrase_{compteur_phrases}"]["tokens_decomp"].update(analyse_line([sent], {}, dico_ne[file][f"phrase_{compteur_phrases}"], dico_gn[f"phrase_{compteur_phrases}"]))
						compteur_phrases += 1
		# print("\n")
		cpxs_gp2[0].append(sum(g2_n_tokens[:-compteur_phrases-1:-1])) # on récupère seulement les éléments du document en cours donc on va en arrière jusqu'à l'index de la dernière phrase du document précédent
		cpxs_gp2[1].append(sum(g2_time_data[:-compteur_phrases-1:-1]))
		cpxs_gp2[2].append(sum(g2_memory_data[:-compteur_phrases-1:-1]))
		# print("\n")
	return dico, cpxs_gp1, cpxs_gp2, cpxs_gp3, cpxs_gp4

def build_conll(dico_global: defaultdict, output_file: str)-> None:
	"""
	Cette fonction prend en entrée un dictionnaire contenant toutes les informations dont on a besoin
	et le chemin d'accès à un fichier de sortie au format CoNLL, et génère le fichier de sortie.
	
	Args:
	- dico_global (defaultdict) : dictionnaire contenant toutes les informations dont on a besoin
	- output_file (str) : chemin d'accès à un fichier de sortie au format CoNLL

	Returns:
	- None
	"""
	with open(output_file, "w") as output:
		output.write("# global.columns = ID FORM POS HEAD DEPREL NAMED_ENTITIES NOUN_PHRASES\n")
		for file, sentence_analysis in dico_global.items():
			for sentence, analysis in sentence_analysis.items() :
				output.write(f"\n# doc_title = {file}\n# sent_id = {file.split('.')[0]}_{sentence}\n# text = {analysis['text']}\n")
				for token, tok_analysis in analysis["tokens_decomp"].items():
					tok_id = token.split("_")[-1]
					form = tok_analysis["form"]
					pos = tok_analysis["pos"]
					head = tok_analysis["head"]
					dep = tok_analysis["dep"]
					ne = tok_analysis["named_entites"]
					gn = tok_analysis["noun_phrase"]
					output.write(f"{tok_id}\t{form}\t{pos}\t{head}\t{dep}\t{ne}\t{gn}\n")


def normalisation_complexity(data:list):
	"""
	Cette fonction prend en entrée une liste de données et renvoie une liste de données normalisées entre 0 et 1.

	Args:
	- data (list) : liste de données à normaliser

	Returns:
	- normalized_data (list) : liste de données normalisées entre 0 et 1
	"""
	data = np.array(data)
	
	# Min-Max Normalization
	min_val = np.min(data)
	max_val = np.max(data)

	if min_val == max_val:
		return [min_val for _ in data]
	normalized_data = (data - min_val) / (max_val - min_val)
	return normalized_data


def get_pipe_complexity(cpx_gp1:list, cpx_gp2:list, cpx_gp3:list, cpx_gp4:list):
	"""
	Cette fonction prend en entrée les listes de complexités de chaque groupe et renvoie une liste de complexités totales pour le pipeline.

	Args:
	- cpx_gp1 (list) : liste de complexités du groupe 1
	- cpx_gp2 (list) : liste de complexités du groupe 2
	- cpx_gp3 (list) : liste de complexités du groupe 3
	- cpx_gp4 (list) : liste de complexités du groupe 4

	Returns:
	- total_time_cpx (list) : liste de complexités totales en temps pour le pipeline
	- total_space_cpx (list) : liste de complexités totales en espace pour le pipeline
	"""
	g1_t_cpx, g1_s_cpx = cpx_gp1
	n_tokens, g2_t_cpx, g2_s_cpx = cpx_gp2
	g3_t_cpx, g3_s_cpx = cpx_gp3[1:3]
	g4_t_cpx = [cpx["temps_complexite"] for cpx in cpx_gp4]
	g4_s_cpx = [cpx["espace_complexite"] for cpx in cpx_gp4]
	
	# normalisation pour que les différentes mesures aient toutes le même poid dans la mesure finale
	normalized_time_cpx = [normalisation_complexity(x) for x in [g1_t_cpx, g2_t_cpx, g3_t_cpx, g4_t_cpx]]
	normalized_space_cpx = [normalisation_complexity(x) for x in [g1_s_cpx, g2_s_cpx, g3_s_cpx, g4_s_cpx]]

	total_time_cpx = [x+y+w+z for x, y, w, z in zip(*normalized_time_cpx)]
	total_space_cpx = [x+y+w+z for x, y, w, z in zip(*normalized_space_cpx)]
	print("tot:", n_tokens, total_time_cpx, total_space_cpx)
	return n_tokens, total_time_cpx, total_space_cpx
	
	
def plot_complexities(list_x_y1_y2:list):
	"""
	Cette fonction crée un graphique pour représenter la complexité en temps et en espace mémoire par rapport au nombre de tokens.

	Args:
	- list_x_y1_y2 (list) : Liste contenant trois sous-listes : la première pour les valeurs de l'axe x (nombre de tokens), la deuxième pour les valeurs de l'axe y1 (temps), et la troisième pour les valeurs de l'axe y2 (espace mémoire).

	Returns:
	- None. La fonction affiche le graphique créé.
	"""
	# Préparation des données de axe x : tri par rapport au nbre de tokens
	combined = list(zip(list_x_y1_y2[0], list_x_y1_y2[1], list_x_y1_y2[2]))
	sorted_on_ntokens = sorted(combined, key=lambda x: x[0])
	nb_toks, temps, espace= zip(*sorted_on_ntokens)
	
	# Suppression des colonnes où il y a des zéros car sûrement une erreur de mesure de complexité
	vec = np.array([nb_toks, temps, espace])
	zero_indices = np.where(vec == 0)[1]
	new_vec = np.delete(vec, zero_indices, axis=1)

	nb_toks = new_vec[0]
	temps = new_vec[1]
	espace = new_vec[2]

	# normalisation par le minimum pour mieux visualiser les pentes des courbes
	temps = [y / min(temps) for y in temps]
	espace = [y / min(espace) for y in espace]
	
	y_fx = [n for n in nb_toks]
	y_fx = [y / min(y_fx) for y in y_fx]
	
	y_logx = [math.log(n) for n in nb_toks]
	y_logx = [y / min(y_logx) for y in y_logx]
 
	y_xlogx = [n * math.log(n) for n in nb_toks]
	y_xlogx = [y / min(y_xlogx) for y in y_xlogx]
 
	# Création de la figure et de l'axe principal
	fig, ax1= plt.subplots()
	
	ax1.set_xlabel('Nombre de tokens')

	# échelle logarithmique pour comparer plus facilement les pentes
	ax1.loglog(nb_toks, temps, color='green', marker='o', linestyle='-', label='Temps')
	ax1.loglog(nb_toks, espace, color='purple', marker='o', linestyle='-', label='Espace mémoire')

	# les fonctions de comparaison
	ax1.loglog(nb_toks, y_fx, linestyle='--', label='O(x)')
	ax1.loglog(nb_toks, y_logx, linestyle='--', label='O(log(x))')
	ax1.loglog(nb_toks, y_xlogx, linestyle='--', label='O(xlog(x)')
	# Titre et légendes
	fig.tight_layout() # Ajuste la mise en page pour éviter les chevauchements
	plt.title('Complexité en temps et espace memoire vs nb de tokens')
	# Affichage
	plt.grid()
	plt.legend()
	plt.subplots_adjust(top=0.9)  # Ajuster pour donner plus d'espace au titre
	plt.savefig("plot_time_space_complexities.png", bbox_inches='tight')
	plt.show()


if __name__=="__main__":
	corpus_path = sys.argv[1] if sys.argv[1][-1] == "/" else sys.argv[1] + "/"
	dico, cpx_gp1, cpx_gp2, cpx_gp3, cpx_gp4 = build_dico(corpus_path)
	
	sys.stdout = sys_stdout
	print("Retour des affichages...")

	list_n_tokens = cpx_gp2[0]
 
	print("1:", cpx_gp1)
	print("2:", cpx_gp2)
	print("3:", cpx_gp3)
	print("4:", cpx_gp4)
 
	# plot_complexities([list_n_tokens, cpx_gp1[0], cpx_gp1[1]])
	# plot_complexities(cpx_gp2)
	# plot_complexities(cpx_gp3)
	plot_complexities(get_pipe_complexity(cpx_gp1, cpx_gp2, cpx_gp3, cpx_gp4))

	

	# print(dico)
	build_conll(dico, sys.argv[2])
