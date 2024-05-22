#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Avec un fichier long (comme notre corpus), vous finirez par avoir des soucis d'erreurs de récursions.
Il y a deux manières de résoudre ce problème:
- augmenter la limite de recursion avec le module sys (à vos risques et périls...)
- transformer le code pour passer d'un code récursif à un code itératif (ce qui n'est pas le but de ce projet)
"""

import time
import spacy
nlp = spacy.load("fr_core_news_sm")

import sys
sys.setrecursionlimit(6000)


def preprocess_file(inputFile: str, cpt_temps) -> list[dict]:
    """ ouvre le fichier texte, le découpe au niveau des '\n'
    et appelle la fonction analyse_spacy() pour analyser le texte

    Args:
        inputFile (str): chemin vers le fichier

    Returns:
        list[dict]: chaque dico correspond à une phrase analysé
    """
    with open(inputFile, 'r') as file:
        texte = [line.rstrip() for line in file.readlines()]
        if len(texte) == 0:
            return [], cpt_temps
        return analyse_spacy(texte, cpt_temps+1)


def analyse_spacy(texte: list[str], cpt_temps) -> list[dict]:
    """ on analyse le texte avec spacy

    Args:
        texte (list[str]): liste de phrase

    Returns:
        list[dict]: chaque dico correspond à une phrase analysé
    """
    docs = list(nlp.pipe(texte, disable=["parser", "lemmatizer", "attribute_ruler"]))
    return process_file([], docs, cpt_temps+1)


def process_file(dicos: list[dict], docs: list[spacy.tokens.doc.Doc], cpt_temps) -> list[dict]:
    """ traite le texte ligne par ligne jusqu'à renvoyer

    Args:
        dicos (list[dict]): chaque dico correspond à une phrase analysé
        docs (list[spacy.tokens.doc.Doc]): liste de phrase analysé avec spacy

    Returns:
        list[dict]: chaque dico correspond à une phrase analysé
    """
    # print("docs", len(docs), cpt_temps)
    if len(docs) == 0:
        return dicos, cpt_temps
    else:
        dicos.append({})
        dicos, cpt_temps = process_line(0, dicos, docs[0], cpt_temps+1)
        return process_file(dicos, docs[1:], cpt_temps+1)


def process_line(i: int, dicos: list[dict], doc: spacy.tokens.doc.Doc, cpt_temps) -> list[dict]:
    """ traite la ligne analysé par spacy pour créer un dico avec comme clé l'index
    du token et comme valeur un tuple (le token, son annotation)

    Args:
        i (int): l'index du token à analyser
        dicos (dict): chaque dico correspond à une phrase analysé
        doc (spacy.tokens.doc.Doc): la ligne analysé par spacy

    Returns:
        list[dict]: chaque dico correspond à une phrase analysé
    """
    # print("doc", len(doc), cpt_temps)
    if len(doc) == 0:
        return dicos, cpt_temps
    else:
        if doc[0].ent_iob_ != "O":
            dicos[-1][i] = (doc[0].text, doc[0].ent_iob_+"-"+doc[0].ent_type_)
        else:
            dicos[-1][i] = (doc[0].text, "O")
        return process_line(i+1, dicos, doc[1:], cpt_temps+1)


if __name__ == "__main__":
    
    start_time = time.time() # début du calcul du temps d'execution
    dicos, temps = preprocess_file("../Corpus/JV-5_semaines_ballon.txt", cpt_temps=1) # on commencence compteur temps à 1 car la fonction est appelé
    end_time = time.time() # fin du calcul du temps d'execution 
    
    print("Les fonctions de ce fichier ont été appelées", temps, "fois pour le fichier 'JV-5_semaines_ballon.txt'.")
    print("Ce fichier python a tourné", round(end_time - start_time, 3), "secondes pour le fichier 'JV-5_semaines_ballon.txt'.")
