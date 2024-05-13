import spacy
import time
from pprint import pprint

# initialiser les variables globales
global memo
memo = {}
global cmpx
cmpx = 0


nlp = spacy.load('fr_core_news_sm')

def ajout_dico(nm, ele):
    global memo
    if nm not in memo : 
        memo[nm] = [len(ele)]
    else :
        memo[nm].append(len(ele))


def spacy_pos_tag_recursive(texte, index_tok=0, tags=None, doc=None):
    global cmpx
    cmpx += 1

    #initialiser s'il n'ya pas de tags, initialiser également doc
    if tags is None:
        tags = {}
        ajout_dico("tags", tags)

    if doc is None:
        #pour ne pas initialiser à chaque appel récursif
        doc = nlp(texte) #appliquer spacy
        ajout_dico("doc", doc)

    #print(len(doc)) --> 447
    #len(texte) compte les caractères pas des mots donc environ 2028
    #le script crachait à index 446 car on retourn tags selon len texte on essaye d'acceder aux mots qui n'existen pas
    #il faut initialiser doc avant

    #si l'index arrive à la fin de la phrase
    if index_tok >= len(doc):
        return tags
    
    token = doc[index_tok] #token
    ajout_dico("token", token)
    token_index_dic = index_tok + 1 #index du token
    tags[token_index_dic] = {token.text: token.pos_} #ajouter le token avec son pos tag dans le dictionnaire
    #tagged_word = (token.text, token.pos_) #token avec pos
    #ajout_dico("tagged_word", tagged_word)
    #tags.append(tagged_word) #rajouter token avec son pos tag dans la liste des tags
    ajout_dico("tags", tags)

    # print(tagged_word) #pour voir

    return spacy_pos_tag_recursive(texte, index_tok + 1, tags, doc) #appel récursif pour itérer sur les mots

#test
with open('petit_test.txt', 'r') as file:
    texte = file.read().replace('\n', '')

start = time.time()
res = spacy_pos_tag_recursive(texte)
pprint(res)
end = time.time()
tot = end - start
print("compléxité en temps : ", tot)

memo_tot=0
for key, values in memo.items():
    memo_tot += max(values)
#l'espace maximal alloué lors traitement
print("compléxité en espace : ", memo_tot, "bytes max. utilisés lors traitement")