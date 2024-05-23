import sys
import os
import glob
import spacy
import csv
import time
import psutil
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple

# Assurez-vous que les chemins sont corrects pour les fonctions importées
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Groupe2')))
from groupe2 import process_gp2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Groupe1')))
from groupe1 import process_gp1, preprocess_gp1


def mesure_complexite(func):
    """
    Décorateur pour mesurer le temps et la mémoire utilisés par une fonction.
    """
    def wrapper(*args, **kwargs):
        debut_temps = time.time()
        debut_memoire = psutil.Process(os.getpid()).memory_info().rss

        resultat = func(*args, **kwargs)

        fin_temps = time.time()
        fin_memoire = psutil.Process(os.getpid()).memory_info().rss

        temps_complexite = fin_temps - debut_temps
        espace_complexite = fin_memoire - debut_memoire

        info_complexite = {
            'temps_complexite': temps_complexite,
            'espace_complexite': espace_complexite
        }

        return resultat, info_complexite

    return wrapper


@mesure_complexite
def process_gp4(nom_fichier: str) -> List[Dict[int, Tuple[spacy.tokens.token.Token, str]]]:
    """
    Traite un fichier texte pour annoter les groupes nominaux avec des tags BIO.
    
    Args:
    - nom_fichier (str): Le chemin vers le fichier texte d'entrée.
    
    Returns:
    - List[Dict[int, Tuple[spacy.tokens.token.Token, str]]]: Une liste de dictionnaires,
      chacun contenant des indices de tokens mappés à des tuples (token, tag BIO).
    """
    res_final = []

    # Obtenir les phrases analysées à partir des fonctions des groupes 1 et 2
    phrases_analysees = process_gp2(process_gp1(preprocess_gp1(nom_fichier)))

    for phrase in phrases_analysees:
        res_intermediaire = {}
        tags_bio_GN = ["O"] * len(phrase)  # Initialiser les tags BIO à 'O'

        # Annoter les chunks nominaux avec des tags BIO
        for chunk in phrase.noun_chunks:
            tags_bio_GN[chunk.start] = "B-GN"
            for i in range(chunk.start + 1, chunk.end):
                tags_bio_GN[i] = "I-GN"

        # Créer le dictionnaire de résultats pour la phrase courante
        for numero_token, (token, tag) in enumerate(zip(phrase, tags_bio_GN)):
            res_intermediaire[numero_token] = (token, tag)
        
        res_final.append(res_intermediaire)

    return res_final


def ecrire_tsv(annotations: List[Tuple[spacy.tokens.token.Token, str]], fichier_sortie: str = 'annotation_GN.tsv'):
    """
    Écrit les annotations dans un fichier TSV.
    
    Args:
    - annotations (List[Tuple[spacy.tokens.token.Token, str]]): Annotations à écrire.
    - fichier_sortie (str): Chemin vers le fichier TSV de sortie.
    """
    with open(fichier_sortie, 'w', newline='') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t')
        for ligne in annotations:
            writer.writerow(ligne)


if __name__ == "__main__":
    # Définir le chemin vers le corpus
    chemin_corpus = os.path.abspath(os.path.join('..', 'Corpus'))
    fichiers_txt = glob.glob(os.path.join(chemin_corpus, '*.txt'))

    # Chemins relatifs pour la sortie
    chemins_relatifs = [os.path.join("..", "Corpus", os.path.basename(chemin)) for chemin in fichiers_txt]
    
    temps_execution = []
    memoire_utilisee = []
    noms_fichiers = []

    # Traiter chaque fichier et mesurer la complexité
    for fichier in chemins_relatifs:
        print(f"Lecture du fichier {fichier}...")
        res, info_complexite = process_gp4(fichier)
        temps_execution.append(info_complexite['temps_complexite'])
        memoire_utilisee.append(info_complexite['espace_complexite'] / (1024 ** 2))  # Convertir en MB
        noms_fichiers.append(os.path.basename(fichier))

        # Afficher quelques résultats pour vérification
        for elt in res[:10]:
            print(elt)

    # Tracer les complexités
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(noms_fichiers, temps_execution, marker='o')
    plt.xticks(rotation=45, ha="right")
    plt.xlabel('Fichiers')
    plt.ylabel('Temps d\'exécution (secondes)')
    plt.title('Temps d\'exécution par fichier')

    plt.subplot(1, 2, 2)
    plt.plot(noms_fichiers, memoire_utilisee, marker='o', color='r')
    plt.xticks(rotation=45, ha="right")
    plt.xlabel('Fichiers')
    plt.ylabel('Mémoire utilisée (MB)')
    plt.title('Mémoire utilisée par fichier')

    plt.tight_layout()
    plt.show()

    # Décommenter pour écrire les fichiers d'annotations
    # for fichier_texte in fichiers_txt:
    #     print(f"Lecture du fichier {os.path.basename(fichier_texte)}...")
    #     nom_fichier_tsv = os.path.join("annotations_GN", os.path.basename(fichier_texte).replace('.txt', '_annotations_GN.tsv'))
    #     annotations, _ = process_gp4(fichier_texte)
    #     print(f"Écriture du fichier {nom_fichier_tsv}...")
    #     ecrire_tsv(annotations, nom_fichier_tsv)

