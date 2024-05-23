#!/bin/python3
import spacy
import time
import tracemalloc
import matplotlib.pyplot as plt
import glob
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Groupe1')))
from groupe1 import process_gp1, preprocess_gp1

nlp = spacy.load("fr_core_news_sm")

tracer_enabled = False
time_data = [] # temps d'exécution
memory_data = [] # mémoire utilisée
n_tokens = []
n = 0 # nombre de tokens

def time_and_memory_wrapper(func):
    """
    Décorateur pour mesurer le temps d'exécution et la mémoire utilisée par une fonction
    
    Args:
        func (callable): La fonction à décorer.
    
    Returns:
        callable: La fonction décorée avec des mesures de temps et de mémoire.
    """
    def wrapper(*args, **kwargs):
        global tracer_enabled, n, time_data, memory_data, n_tokens # Il est plus prudent de les réinitialiser à ce moment-là Shami
        # Démarre le traçage de la mémoire si ce n'est pas déjà fait
        if not tracer_enabled:
            tracemalloc.start()
            tracer_enabled = True
        
        # Mesure de la mémoire et du temps avant et après l'exécution de la fonction    
        snapshot_id0 = tracemalloc.take_snapshot()
        start_time = time.time()
        result = func(*args, **kwargs)
        # result = str([item for sublist in result for item in sublist]).split()
        snapshot_id1 = tracemalloc.take_snapshot()
        end_time = time.time()

        # Calcul et enregistrement des différences de mémoire et de temps, ainsi que du nombre de tokens
        mem_diff = snapshot_id1.compare_to(snapshot_id0, 'lineno')
        time_data.append(end_time - start_time)
        memory_data.append(sum(block.size for block in mem_diff)/10**6)

        # maj nombre de tokens
        token_count = sum(len(doc) for doc in result)
        n_tokens.append(token_count)
        n += token_count

        # Affiche les informations de performance pour la fonction
        print(f"Function {func.__name__} took {end_time - start_time} seconds\n and used {sum(block.size for block in mem_diff)/10**6} MB of memory")

        # Arrête le traçage de la mémoire si il était activé
        if tracer_enabled:
            tracemalloc.stop()
            tracer_enabled = False

        return result
    return wrapper

def plot_complexity():
    """
    Fonction pour tracer les données de complexité en temps et en mémoire
    
    Utilise les listes globales `n_tokens`, `time_data` et `memory_data` 
    pour créer un graphique combiné avec deux axes x, y,
    x : représente le nombre de tokens.
    y : représente le temps d'exécution.
    """
    # Tri des trois listes sur le nombre de tokens
    combined = list(zip(n_tokens, time_data, memory_data))
    sorted_on_ntokens = sorted(combined, key=lambda x: x[0])
    n_tokens_sorted, time_data_sorted, memory_data_sorted = zip(*sorted_on_ntokens)

    # Création du premier diagramme pour l'axe de gauche (temps)
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Number of tokens')
    ax1.set_ylabel('Time (s)', color=color)
    line1, = ax1.plot(n_tokens_sorted, time_data_sorted, label='Time (actual)', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Création du deuxième diagramme pour l'axe de droite (mémoire)
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Memory (MB)', color=color)
    line2, = ax2.plot(n_tokens_sorted, memory_data_sorted, label='Memory (actual)')
    ax2.tick_params(axis='y', labelcolor=color)

    # Affichage de la légende
    lines = [line1, line2]
    ax1.legend(lines, [line.get_label() for line in lines], loc='upper left')

    # Affichage du diagramme à l'écran
    fig.tight_layout()
    plt.grid()
    plt.savefig('complexity.png')
    #plt.pause(15)
    #plt.close('all')
    plt.show()

@time_and_memory_wrapper
def process_gp2(docs):
    """
    Fonction pour traiter les documents avec le pipeline de traitement NLP de Spacy
    
    Args:
        docs (list): Liste de documents textuels à traiter.

    Returns:
        list : tok.text, tok.pos_, tok.dep_, tok.head

    """
    res = list(nlp.pipe(docs, disable=["morphologizer", "ner", "lemmatizer", "attribute_ruler"]))
    return res

# Ne s'exécute pas dans le cas d'import de module
if __name__ == "__main__":
    input_files = glob.glob('../Corpus/*.txt') # tout les fichiers dans le dossier Corpus
    for input_file in input_files:
        # Préprocessus et processus de chaque fichier, puis mesure des performances
        process_gp2(process_gp1(preprocess_gp1(input_file)))
        print(f"Processing {input_file}...")

    print(f"Total number of tokens: {n}")
    print("Time data:", time_data)
    print("Memory data:", memory_data)
    
    # Génère et affiche le graphique de complexité
    plot_complexity()
                