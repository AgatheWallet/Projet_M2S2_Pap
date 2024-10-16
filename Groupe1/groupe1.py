import spacy
import time
import pprint
import glob
import json
import sys 

# augmenter la limite de récursivite car les fichiers sont grands
sys.setrecursionlimit(10000)

# charger le modèle spacy
nlp = spacy.load("fr_core_news_sm")

# initialiser les variables globales
global memo
memo = {}

# lire le(s) fichier(s)
def preprocess_gp1(inputFile):
    """
    files = glob.glob(inputFile + "/*.txt")
    textes = []
    for inputFile in files:
        with open(inputFile, 'r', encoding='utf-8') as file:
            textes.extend(file.readlines())
            textes = [texte.replace('\n', '') for texte in textes]
    return textes
    """
    with open(inputFile, 'r') as file:
        textes = file.readlines()
        textes = [text.replace('\n', '') for text in textes]   
        return textes


def process_gp1(textes) :
    """Une fonction de traitement du text avec module Spacy"""
    res = list(nlp.pipe(textes, disable=["parser", "ner", "lemmatizer", "attribute_ruler"]))
    return res


def recursive_objet_doc(docs, index_doc=0, all_tags=None):
    """Une fonction qui récupère toutes les annotations des objets doc"""
	
	# initialisation d'une liste qui va contenir des dictionnaires d'annotation
    if all_tags == None : 
        all_tags=[]

	# index pour la récursivité
    if index_doc >= len(docs) :
        return all_tags
    
    #récupèration d'un doc
    doc = docs[index_doc]
    
    # appel de fonction récursive pour obtenir des annotations dans le doc
    tags = recursive_tokens_pos(doc)
    
    # ajout des annotations
    all_tags.append(tags)
    
    return recursive_objet_doc(docs, index_doc + 1, all_tags)


def ajout_dico(nm, ele):
    """Une fonction pour ajouter des éléments et leurs longueurs dans le dictionnaire pour faciliter le calcul de compléxité"""
    global memo
    if nm not in memo : 
        memo[nm] = [len(ele)]
    else :
        memo[nm].append(len(ele))


def recursive_tokens_pos(doc, index_tok=0, tags=None):
    """Une fonction qui récupère les pos tags des tokens"""

    #initialiser s'il n'ya pas de tags, initialiser également doc
    if tags is None:
        tags = {}
        # ajout_dico("tags", tags)

    #si l'index arrive à la fin de la phrase
    if index_tok >= len(doc):
        ajout_dico("tags", tags)
        return tags
    
    token = doc[index_tok] #token
    token_index_dic = index_tok + 1 #index du token

	#ajouter le token avec son pos tag dans le dictionnaire
    tags[token_index_dic] = {token.text: token.pos_} 

    return recursive_tokens_pos(doc, index_tok + 1, tags) #appel récursif pour itérer sur les mots

def save_json(res):
    """Une fonction pour sauvegarder les résultats dans un fichier json"""
    with open('./resultat_groupe1_JV-Tour_monde.json', 'w') as sortie_json:
        json.dump(res, sortie_json, indent=6, ensure_ascii=False)

def get_complexity_time(fichier, json=False):
    """Une fonction pour obtenir la compléxité en temps et sauvegarder les résultats dans un fichier json"""
    global tot
    global memo 
    memo = {} #réinitialiser le dictionnaire pour chaque fichier

    # calcul de complexité en temps
    start = time.time()
    res = recursive_objet_doc(process_gp1(preprocess_gp1(fichier))) #proccessing
    end = time.time()
    tot = end - start
    print("compléxité en temps : ", tot)

    # sauvegarder le fichier processé dans un fichier json
    if json:
        save_json(res)
    return tot

def get_complexity_space():
    """Une fonction pour obtenir la compléxité en espace"""
    global memo_f
    memo_f = 0
    for key, values in memo.items():
        if key == "tags":
            memo_f += sum(values)
    memo_f2 = memo_f * 2 #car chaque élément dans le dictionnaire contient deux éléments présenté comme cle:valeur mais on ne compte que les valeurs

    print("compléxité en espace :", memo_f, "tuples de pos tag")
    print("compléxité en espace :", memo_f2, "éléments dans la mémoire")
    return memo_f

if __name__ == "__main__":
    fichier_du_corpus = "../Corpus/JV-Tour_monde.txt"
    print("Fichier traité : ", fichier_du_corpus.split("/")[-1])
    get_complexity_time(fichier_du_corpus, json=True) #calcul de complexité en temps
    get_complexity_space() #calcul de complexité en espace
