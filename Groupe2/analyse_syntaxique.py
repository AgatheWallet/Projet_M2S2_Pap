#!/bin/python3
import spacy

nlp = spacy.load("fr_core_news_sm")


def preprocess_gp1(inputFile):
    with open(inputFile, 'r') as file:
        textes = file.readlines()
        print(nlp.pipeline)
        return textes

def process_gp1(textes):
    res = list(nlp.pipe(textes, disable=["parser", "ner", "lemmatizer", "attribute_ruler"]))
    """
    for doc in res:
        for tok in doc:
            print(tok.text, tok.pos_)
    """
    return res
# On n'enlève pas morphologizer, car c'est le module qui POS tag.


def process_gp2(docs):
    res = list(nlp.pipe(docs, disable=["morphologizer", "ner", "lemmatizer", "attribute_ruler"]))
    """
    for doc in res:
        for tok in doc:
            print(tok.text, tok.pos_, tok.dep_, tok.head)
    """
    return res

process_gp2(process_gp1(preprocess_gp1('petit_test.txt')))