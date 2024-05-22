#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Avec un fichier long (comme notre corpus), vous finirez par avoir des soucis d'erreurs de récursions.
Il y a deux manières de résoudre ce problème:
- augmenter la limite de recursion avec le module sys (à vos risques et périls...)
- transformer le code pour passer d'un code récursif à un code itératif (ce qui n'est pas le but de ce projet)
Calcul de complexité avec ajout de 2 paramètres : un pour la complexité en espace et un pour la complexité en temps
"""

import spacy
nlp = spacy.load("fr_core_news_sm")

import sys
sys.setrecursionlimit(6000)


def preprocess_file(inputFile: str, cpt_def, cpt_espace, cpt_temps) -> tuple[list[dict], int, int]:
	""" ouvre le fichier texte, le découpe au niveau des '\n'
	et appelle la fonction analyse_spacy() pour analyser le texte
	Args:
		inputFile (str): chemin vers le fichier
	Returns:
		1 dico = 1 SpacyDoc = 1 phrase analysée
		tuple : (list[], cpt_espace, cpt_temps) ou tuple (list[dict[i:(tok,label)]], cpt_espace, cpt_temps)
	"""
	with open(inputFile, 'r') as file:
		texte = [line.rstrip() for line in file.readlines()] # list[str]
		if len(texte) == 0:
			cpt_temps += 1
			return [], cpt_espace, cpt_temps
		cpt_temps += 1
# 		print(f'cpt_temps dans preprocess_file : {cpt_temps}')
		print(f' cpt_espace dans preprocess_file : {cpt_espace}')
		return analyse_spacy(texte, cpt_def, cpt_espace, cpt_temps)


def analyse_spacy(texte: list[str], cpt_def, cpt_espace, cpt_temps) -> tuple[list[dict], int, int]:
	""" Création d'un objet SpacyDoc par ligne (donc phrase) du texte original
	Args:
		texte (list[str]): liste de phrases
	Returns:
		1 dico = 1 SpacyDoc = 1 phrase analysée
		tuple (list[dict[i:(tok,label)]] , cpt_espace, cpt_temps)
	"""
	docs = list(nlp.pipe(texte, disable=["parser", "morphologizer", "lemmatizer", "attribute_ruler"])) # list[SpacyDoc]
	cpt_temps += 1
# 	print(f'cpt_temps dans analyse_spacy : {cpt_temps}')
	return process_file([], docs, cpt_def, cpt_espace, cpt_temps)


def process_file(dicos: list[dict], docs: list[spacy.tokens.doc.Doc], cpt_def, cpt_espace, cpt_temps) -> tuple[list[dict], int, int]:
	""" 
	traite les SpacyDocs (donc le texte ligne par ligne) et renvoie les dic[i:(tok,label)] de la def appelée process_line()
	i: indice dans la phrase.
	Args:
		docs (list[spacy.tokens.doc.Doc]): liste de SpacyDocs (de phrases analysées avec Spacy)
	Returns:
		tuple (list[dict[:]] , cpt_espace, cpt_temps) ou 
		tuple (list[dict[i:(tok,label)]] , cpt_espace, cpt_temps)
	"""
	# Alice : si je définis cpt_def = len(docs) + len(dicos) au début de la fonction
	# soit avant le len(docs) == 0, et que je fais le test avant len(docs) == 0
	# j'obtiens un cpteur_espace final = le plus grand nbre de tok dans une phrase (cpt_espace = 126 pour le petit_test)
	# si je définis cpt_def = len(dicos) (pareil que len(docs) + len(dicos) puisque len(doc)==0)
	# j'obtiens un cpteur espace fnal qui inclut le nbre de tous les tokens (cpt_espace = 447 dont 358 toks pour le petit_test
	# ce qui me paraît plus proche de ce que qu'on veut ? j'ai donc laissé le test au niveau du if len(doc)==0
	if len(docs) == 0: 
		cpt_def = len(dicos) # qd plus de docs (SpacyDoc) on a rempli la liste des dicos
		print(f'cpt_def in process_file() ajout len(dicos) : {cpt_def}')
		if cpt_def > cpt_espace:
			cpt_espace = cpt_def
			print(f'cpt def > cpt_espace : {cpt_espace}')
		return dicos, cpt_espace, cpt_temps
	else:
		dicos.append({})
		cpt_temps += 1
		dicos, cpt_def, cpt_espace, cpt_temps = process_line(0, dicos, docs[0], cpt_def, cpt_espace, cpt_temps	)
		cpt_temps +=1
# 		print(f'cpt_temps dans process_file : {cpt_temps}')
		return process_file(dicos, docs[1:], cpt_def, cpt_espace, cpt_temps) 


def process_line(i: int, dicos: list[dict], doc: spacy.tokens.doc.Doc, cpt_def, cpt_espace, cpt_temps) -> list[dict]:
	""" traite le SpacyDoc pour remplir un dico avec comme clé l'index
	du token et comme valeur un tuple (le token, son annotation)
	Args:
		i (int): l'index du token à analyser
		dicos (dict): chaque dico correspond à une phrase analysé
		doc (spacy.tokens.doc.Doc): la ligne analysée par Spacy 
	Returns:
		list[dict]: chaque dico correspond à une phrase analysée
	"""
	if i == 0: # on est au 1er tok , else : on a commencé à enlever des élé de la liste
		cpt_def += len(doc) # nbre de toks
		print(f'cpteur_def += len(doc) : {len(doc)}')
		if cpt_def > cpt_espace:
			cpt_espace = cpt_def
			print(f'cpt_def in process_line() > cpt_espace : {cpt_espace}')
		# LAURA : c'est ça !
		# LAURA : maintenant tu vérifies si cpt_def est plus grand que cpt_espace
		# LAURA : tu n'as pas besoin de le faire ailleurs dans la fonction car len(doc)
		# LAURA : ne fait que baisser après ça donc cpt_def ne peux plus être plus grand 
		# LAURA : que cpt_espace
		# LAURA : je dirais même que tu n'est plus obligé de faire -1 à chaque appel de fonction
		# LAURA : car de toute façon la taille de l'espace mémore de doc disparait au
		# LAURA : début de la fonction process_file
	if len(doc) == 0: # fin lecture du SpacyDoc
	return dicos, cpt_def, cpt_espace, cpt_temps
	else:
		if doc[0].ent_iob_ != "O":
			dicos[-1][i] = (doc[0].text, doc[0].ent_iob_+"-"+doc[0].ent_type_)
		else:
			dicos[-1][i] = (doc[0].text, "O")
	# 		cpt_temps +=1
	# 		print(f'cpt_temps dans process_line : {cpt_temps}')
		return process_line(i+1, dicos, doc[1:], cpt_def, cpt_espace, cpt_temps)


if __name__ == "__main__":
	print(preprocess_file("petit_test.txt", cpt_def=0, cpt_espace=0, cpt_temps=0))
	#print(preprocess_file("../Corpus/JV-5_semaines_ballon.txt"))
