import spacy
import time
import pprint
import glob

nlp = spacy.load("fr_core_news_sm")
# initialiser les variables globales
global memo
memo = {}


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


def process_gp1(textes):
    res = list(nlp.pipe(textes, disable=["parser", "ner", "lemmatizer", "attribute_ruler"]))
    return res


def recursive_pos_tagging(docs, index_doc=0, all_tags=None):
    if all_tags == None : 
        all_tags=[]

    if index_doc >= len(docs) : 
        return all_tags
    
    doc = docs[index_doc]
    tags = spacy_pos_tag_recursive(doc)
    all_tags.append(tags)
    index_doc += 1

    ajout_dico("all_tags", all_tags)
    return recursive_pos_tagging(docs, index_doc, all_tags)


def ajout_dico(nm, ele):
    global memo
    if nm not in memo : 
        memo[nm] = [len(ele)]
    else :
        memo[nm].append(len(ele))


def spacy_pos_tag_recursive(doc, index_tok=0, tags=None):
    #initialiser s'il n'ya pas de tags, initialiser également doc
    if tags is None:
        tags = {}
        # ajout_dico("tags", tags)

    #si l'index arrive à la fin de la phrase
    if index_tok >= len(doc):
        ajout_dico("tags", tags)
        return tags
    
    token = doc[index_tok] #token
    ajout_dico("token", token)
    token_index_dic = index_tok + 1 #index du token

    tags[token_index_dic] = {token.text: token.pos_} 
    #ajouter le token avec son pos tag dans le dictionnaire

    return spacy_pos_tag_recursive(doc, index_tok + 1, tags) #appel récursif pour itérer sur les mots

if __name__ == "__main__" :
    start = time.time()
    res = recursive_pos_tagging(process_gp1(preprocess_gp1('petit_test.txt')))
    print(res)
    end = time.time()
    tot = end - start
    print("compléxité en temps : ", tot)


    memo_f = 0
    for key, values in memo.items():
        if key == "tags":
            memo_f += sum(values)
    memo_f2 = memo_f*2

    print("compléxité en espace :", memo_f, "tuples de pos tag")
    print("compléxité en espace :", memo_f2, "elements dans la mémoire")
