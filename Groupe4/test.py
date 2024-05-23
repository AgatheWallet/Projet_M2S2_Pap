import sys, os, glob, spacy, csv
from typing import List, Dict, Tuple
import time
import psutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Groupe2')))
from groupe2 import process_gp2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Groupe1')))
from groupe1 import process_gp1, preprocess_gp1


def measure_complexity(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process(os.getpid()).memory_info().rss

        result = func(*args, **kwargs)

        end_time = time.time()
        end_memory = psutil.Process(os.getpid()).memory_info().rss

        time_complexity = end_time - start_time
        space_complexity = end_memory - start_memory

        complexity_info = {
            'time_complexity': time_complexity,
            'space_complexity': space_complexity
        }

        return result, complexity_info

    return wrapper


@measure_complexity
def process_gp4(filename:str) -> List[Dict[int, Tuple[spacy.tokens.token.Token, str]]]:
    """
        À partir du nom du fichier texte donné en entrée,
        renvoie un dictionnaire avec la structure suivante :

        { numéro_de_token : (token_spacy, annotation_groupe_nominale) }

        avec les conventions :
        * B-GN (begin groupe nominal) pour le premier 
        * I-GN ensuite
        * O sinon        
    """

    res_final = []

    # on récupère les données du groupe 2 (objets spacy)
    phrases_analysees = process_gp2(process_gp1(preprocess_gp1(filename)))

    for phrase in phrases_analysees:
        # annotations de la phrase courante
        res_intermediaire = {}

        print(phrase)

        # liste des tags BIO pour les groupes nominaux
        tags_bio_GN = ["O"] * len(phrase)

        # on parcout les groupes nominaux
        for chunk in phrase.noun_chunks:
            tags_bio_GN[chunk.start] = "B-GN" # le premier
            for i in range(chunk.start + 1, chunk.end): # les suivants
                tags_bio_GN[i] = "I-GN"

        # on rassemble en tuples
        numero_token = 0 # on commence à compter à zéro 
        for token, tag in zip(phrase, tags_bio_GN):
            res_intermediaire[numero_token] = (token, tag)
            numero_token += 1
            #print(f"{token.text}\t{tag}")
        
        # on a fini de traiter la phrase, on ajoute le dico des annotations à la liste finale
        res_final.append(res_intermediaire)
    
    # on a traité toutes les phrases
    return res_final 

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

    # pour avoir les chemins relatifs
    chemins_relatifs = [ "../Corpus/" + chemin.split('/')[-1] for chemin in txt_files]
    
    test = chemins_relatifs[0]

    print(f"Lecture du fichier {test}...")

    res, complexity_info = process_gp4(test)

    for elt in res[0:10]:
        print(elt)

    print(f"Temps d'exécution : {complexity_info['time_complexity']:.4f} secondes")
    print(f"Mémoire utilisée : {complexity_info['space_complexity'] / 131072:.4f} Mb")
    
    #for fichier_texte in txt_files:
    #    print(f"Lecture du fichier {fichier_texte.split('/')[-1]}...")
    #    nom_fichier_tsv = "annotations_GN/" + fichier_texte.split('/')[-1].split('.')[0] + "_annotations_GN.tsv"
    #    annotations = process_gp4(str(fichier_texte))
    #    print(f"Écriture du fichier {nom_fichier_tsv}...")
    #    write_tsv(annotations, nom_fichier_tsv)
