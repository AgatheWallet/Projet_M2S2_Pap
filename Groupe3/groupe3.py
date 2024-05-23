#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Avec un fichier long (comme notre corpus), vous finirez par avoir des soucis d'erreurs de récursions.
Il y a deux manières de résoudre ce problème:
- augmenter la limite de recursion avec le module sys (à vos risques et périls...)
- transformer le code pour passer d'un code récursif à un code itératif (ce qui n'est pas le but de ce projet)

Le formatage des résultats a été discuté et approuvé par le groupe 5
"""

import time
import spacy
import json
from glob import glob
nlp = spacy.load("fr_core_news_sm")

import sys
sys.setrecursionlimit(6000)


def preprocess_file(inputFile: str, cpt_temps: int, cpt_espace: int) -> list[dict]:
    """ ouvre le fichier texte, le découpe au niveau des '\n',
    supprime les lignes vides et appelle la fonction analyse_spacy() 
    pour analyser le texte

    Args:
        inputFile (str): chemin vers le fichier
        cpt_temps (int): compteur pour la complexité en temps
        cpt_espace (int): compteur pour la complexité en espace

    Returns:
        tuple(): un dico de dicos où chaque dico correspond à une phrase analysé + les compteurs
    """
    with open(inputFile, 'r') as file:
        texte = [line.rstrip() for line in file.readlines() if line.rstrip() != ""]
        if len(texte) == 0:
            return [], cpt_temps, cpt_espace
        # 'textes' est une liste de ligne présente
        # jusqu'à la fin de l'execution du programme 
        # on l'ajoute donc a notre compteur
        cpt_espace = len(texte)
        return analyse_spacy(texte, cpt_temps+1, cpt_espace)


def analyse_spacy(texte: list[str], cpt_temps: int, cpt_espace: int) -> list[dict]:
    """ on analyse le texte avec spacy

    Args:
        texte (list[str]): liste de phrase
        cpt_temps (int): compteur pour la complexité en temps
        cpt_espace (int): compteur pour la complexité en espace
        
    Returns:
        tuple(): chaque dico de dicos correspond à une phrase analysé + les compteurs
    """
    docs = list(nlp.pipe(texte, disable=["parser", "lemmatizer", "attribute_ruler"]))
    # 'docs' contient le texte analysé par spacy, on rajoute le nombre d'élément dans la variable 'cpt_espace'
    # on ne calcule pas seulement le nombre d'élément dans docs, mais le nombre d'éléments dans chaque élément de docs
    cpt_espace += sum([len(doc) for doc in docs])
    # le nombre de tokens selon la tokenisation de spacy
    nb_tokens = sum([len(doc) for doc in docs])
    return process_file([], docs, cpt_temps+1, cpt_espace), nb_tokens


def process_file(dicos: list[dict], docs: list[spacy.tokens.doc.Doc], cpt_temps: int, cpt_espace: int) -> list[dict]:
    """ traite le texte ligne par ligne jusqu'à renvoyer

    Args:
        dicos (list[dict]): chaque dico correspond à une phrase analysé
        docs (list[spacy.tokens.doc.Doc]): liste de phrase analysé avec spacy
        cpt_temps (int): compteur pour la complexité en temps
        cpt_espace (int): compteur pour la complexité en espace

    Returns:
        tuple(): chaque dico de dicos correspond à une phrase analysé + les compteurs
    """
    # lorsqu'une nouvelle phrase analysée apparaît dans la liste 'dicos'
    # elle est supprimé de la liste 'docs' à la ligne d'après
    # donc on doit calculé si à la ligne 72, cpt_espace est plus grand au plus petit 
    if len(docs) == 0:
        return dicos, cpt_temps, cpt_espace
    else:
        dicos.append({})
        dicos, cpt_temps, cpt_espace = process_line(0, dicos, docs[0], cpt_temps+1, cpt_espace)
        # len(textes) == len(dicos)+len(docs)-1
        # cpt_def = len(textes)+len(docs)+len(dicos)
        cpt_def = (len(dicos)+len(docs)-1)+sum([len(doc) for doc in docs])+sum([1 for dico in dicos for token in dico.keys()])
        if cpt_def > cpt_espace:
            cpt_espace = cpt_def
        return process_file(dicos, docs[1:], cpt_temps+1, cpt_espace)


def process_line(i: int, dicos: list[dict], doc: spacy.tokens.doc.Doc, cpt_temps: int, cpt_espace: int) -> list[dict]:
    """ traite la ligne analysé par spacy pour créer un dico avec comme clé l'index
    du token et comme valeur un tuple (le token, son annotation)

    Args:
        i (int): l'index du token à analyser
        dicos (dict): chaque dico correspond à une phrase analysé
        doc (spacy.tokens.doc.Doc): la ligne analysé par spacy
        cpt_temps (int): compteur pour la complexité en temps
        cpt_espace (int): compteur pour la complexité en espace

    Returns:
        tuple(): chaque dico de dicos correspond à une phrase analysé + les compteurs
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
    
def get_complexities(files):
    """ Cette fonction permet d'obtenir les complexités pour chacun des fichiers du corpus.
        Il renvoie une liste de trois listes pour les tokens, la complexité en temps, la complexité en espace 
    """
    # chemins relatifs pour que le groupe 5 puisse facilement appelé sans bug
    complexities = [[], [], []]
    for file in glob(f"{files}*.txt"):
        
        start_time = time.time() # début du calcul du temps d'execution
        (dicos, temps, espace), nb_tokens = preprocess_file(file, cpt_temps=1, cpt_espace=0) # on commencence compteur temps à 1 car la fonction est appelé
        end_time = time.time() # fin du calcul du temps d'execution
        
        complexities[0].append(nb_tokens)
        complexities[1].append(round(end_time - start_time, 3))
        complexities[2].append(espace)
        
        print("\nPour le fichier", file, ":")
        print(f"Les fonctions ont été appelées", temps, "fois.")
        print("Les fonctions auront tourné", round(end_time - start_time, 3), "secondes.")
        print("Dans l'espace mémoire, il y a eu au maximum", espace, "éléments à un moment T.")
        print("Ce fichier fait", nb_tokens, "tokens.")
        
    return complexities

def get_annotations(files):
    """ Cette fonction print dans des fichiers le résultat de notre traitement
    """
    all_dicos = {}
    for file in glob(f"{files}*.txt"):
        (dicos, temps, espace), nb_tokens = preprocess_file(file, cpt_temps=1, cpt_espace=0)
        all_dicos[file] = {}
        for i, dico in enumerate(dicos):
            all_dicos[file]["phrase_"+str(i)] = dico

    return all_dicos

if __name__ == "__main__":
    
    complex = get_complexities(sys.argv[1])
    print(complex)
    
    all_dicos = get_annotations(sys.argv[1])
    with open('annotations_EN.json', 'w', encoding='utf-8') as file:
        json.dump(all_dicos, file, ensure_ascii=False, indent=4)
    