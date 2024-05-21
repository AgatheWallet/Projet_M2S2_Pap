#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Avec un fichier long (comme notre corpus), vous finirez par avoir des soucis d'erreurs de récursions.
Il y a deux manières de résoudre ce problème:
- augmenter la limite de recursion avec le module sys (à vos risques et périls...)
- transformer le code pour passer d'un code récursif à un code itératif (ce qui n'est pas le but de ce projet)
"""

import spacy
nlp = spacy.load("fr_core_news_sm")

import sys
sys.setrecursionlimit(6000)


def preprocess_file(inputFile: str, cpt_analyse_spacy, cpt_process_file, cpt_process_line, cpt_espace) -> list[dict]:
	""" ouvre le fichier texte, le découpe au niveau des '\n'
	et appelle la fonction analyse_spacy() pour analyser le texte
	Args:
		inputFile (str): chemin vers le fichier
	Returns:
		list[dict]: chaque dico correspond à une phrase analysé
	"""
	with open(inputFile, 'r') as file:
		texte = [line.rstrip() for line in file.readlines()] # list[str]
		if len(texte) == 0:
			return []
		return analyse_spacy(texte, cpt_analyse_spacy, cpt_process_file, cpt_process_line, cpt_espace)


def analyse_spacy(texte: list[str], cpt_analyse_spacy, cpt_process_file, cpt_process_line, cpt_espace) -> list[dict]:
	""" on analyse le texte avec spacy : création d'un objet SpacyDoc par ligne/phrase du texte original
	Args:
		texte (list[str]): liste de phrases
	Returns:
		list[dict]: chaque dico correspond à une phrase analysée
	"""
	docs = list(nlp.pipe(texte, disable=["parser", "morphologizer", "lemmatizer", "attribute_ruler"])) # list[SpacyDoc]
	cpt_analyse_spacy += len(docs)
	print(f'cpt_analyse_spacy : {cpt_analyse_spacy}')
	print(f'cpt_espace : {cpt_espace}')
	if cpt_analyse_spacy > cpt_espace:
		cpt_espace += cpt_analyse_spacy
		print(f'cpt_espace : {cpt_espace}')
		print(f'cpt_analyse_spacy > cpt_espace : {cpt_espace}')
	return process_file([], docs, cpt_process_file, cpt_process_line, cpt_espace)


def process_file(dicos: list[dict], docs: list[spacy.tokens.doc.Doc], cpt_process_file, cpt_process_line, cpt_espace) -> list[dict]:
	""" traite le texte ligne par ligne jusqu'à renvoyer
	Args:
		dicos (list[dict]): chaque dico correspond à une phrase analysé
		docs (list[spacy.tokens.doc.Doc]): liste de phrases analysées avec Spacy
	Returns:
		list[dict]: chaque dico correspond à une phrase analysée
	"""
	if len(docs) == 0:
		cpt_process_file += len(dicos)
		print(f'cpt_process_file ajout len(dicos) : {cpt_process_file}')
		if cpt_process_file > cpt_espace:
			cpt_espace += cpt_process_file
			print(f'cpt process_file > cpt_espace : {cpt_espace}')
		return dicos
	else:
		dicos.append({})
		dicos = process_line(0, dicos, docs[0], cpt_process_line, cpt_espace) # cpt_temps +1 ici aussi
		# cpt_time +=1
		return process_file(dicos, docs[1:], cpt_process_file, cpt_process_line, cpt_espace) 


def process_line(i: int, dicos: list[dict], doc: spacy.tokens.doc.Doc, cpt_process_line, cpt_espace) -> list[dict]:
	""" traite la ligne analysée par spacy pour créer un dico avec comme clé l'index
	du token et comme valeur un tuple (le token, son annotation)
	Args:
		i (int): l'index du token à analyser
		dicos (dict): chaque dico correspond à une phrase analysé
		doc (spacy.tokens.doc.Doc): la ligne analysée par Spacy
	Returns:
		list[dict]: chaque dico correspond à une phrase analysée
	"""
	if i == 0: # on est au 1er tok , else : on a commencé à enlever des élé de la liste
		cpt_process_line += len(doc) # initialise ici le cpteur avec la taille du spacyDoc car on cpte opé sur chque token
		print(f'cpt_process_line ajout len(doc) : {len(doc)}')
	if len(doc) == 0:
		# Voir si déplacement du cpteur au niveau du cpte du token ?
		print(f'cpt_process_line + len(dicos) : {cpt_process_line}')
		if cpt_process_line > cpt_espace:
			cpt_espace += cpt_process_line
			print(f'cpt process_line > cpt_espace : {cpt_espace}')
		return dicos
	else:
		if doc[0].ent_iob_ != "O":
			dicos[-1][i] = (doc[0].text, doc[0].ent_iob_+"-"+doc[0].ent_type_)
		else:
			dicos[-1][i] = (doc[0].text, "O")
		cpt_process_line -= 1 # on décrémente la liste des tokens
		return process_line(i+1, dicos, doc[1:], cpt_process_line, cpt_espace)


if __name__ == "__main__":
	preprocess_file("petit_test.txt", cpt_analyse_spacy=0, cpt_process_file=0, cpt_process_line=0, cpt_espace=0)
	#print(preprocess_file("../Corpus/JV-5_semaines_ballon.txt"))
