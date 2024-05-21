import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Groupe2')))
from groupe2 import process_gp2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Groupe1')))
from groupe1 import process_gp1, preprocess_gp1

filename = "../Corpus/JV-Tour_monde.txt"

process_gp2(process_gp1(preprocess_gp1(filename)))

# problème : ne nous donne pas la représentation spacy de l'analyse en dépendances