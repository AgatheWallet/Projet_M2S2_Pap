import sys, os, glob, spacy, csv
from typing import List, Dict, Tuple
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Groupe2')))
from groupe2 import process_gp2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Groupe1')))
from groupe1 import process_gp1, preprocess_gp1

def process_gp4(filename:str) -> List[Tuple[spacy.tokens.token.Token, str]]:
    """
        À partir du nom du fichier texte,
        renvoie une liste de couples (token_spacy, annotatio_BIO_groupe_nominal)

        Avec :
        * B-GN (begin groupe nominal) pour le premier 
        * I-GN ensuite
        * O sinon
    """

    res = []

    # on récupère les données du groupe 2 
    phrases_analysees = process_gp2(process_gp1(preprocess_gp1(filename)))

    for phrase in phrases_analysees:
        # liste des tags BIO pour les groupes nominaux
        tags_bio_GN = ["O"] * len(phrase)

        # on parcout les groupes nominaux
        for chunk in phrase.noun_chunks:
            tags_bio_GN[chunk.start] = "B-GN" # le premier
            for i in range(chunk.start + 1, chunk.end): # les suivants
                tags_bio_GN[i] = "I-GN"

        # on rassemble en tuples
        for token, tag in zip(phrase, tags_bio_GN):
            res.append((token.text, tag))
            #print(f"{token.text}\t{tag}")
        
    return res

def write_tsv(annotations: List[Tuple[spacy.tokens.token.Token, str]], output_file: str = 'annotation_GN.tsv'):
    """
        Écrit la sortie du script précédent dans un fichier .tsv
        dans un fichier nommé output_file
        situé dans le dossier annotations_GN/
    """
    with open(output_file, 'w') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t')
        for ligne in annotations:
            writer.writerow(ligne)

if __name__ == "__main__":
    # on lit tous les fichiers txt du dossier Corpus/
    corpus_path = os.path.abspath(os.path.join('..', 'Corpus'))
    sys.path.append(corpus_path)
    txt_files = glob.glob(os.path.join(corpus_path, '*.txt'))

    for fichier_texte in txt_files:
        print(f"Lecture du fichier {fichier_texte.split('/')[-1]}...")
        nom_fichier_tsv = "annotations_GN/" + fichier_texte.split('/')[-1].split('.')[0] + "_annotations_GN.tsv"
        annotations = process_gp4(str(fichier_texte))
        print(f"Écriture du fichier {nom_fichier_tsv}...")
        write_tsv(annotations, nom_fichier_tsv)

