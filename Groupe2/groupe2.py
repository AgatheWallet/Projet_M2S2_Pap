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
    def wrapper(*args, **kwargs):
        global tracer_enabled, n, time_data, memory_data, n_tokens # Il est plus prudent de les réinitialiser à ce moment-là Shami
        if not tracer_enabled:
            tracemalloc.start()
            tracer_enabled = True

        snapshot_id0 = tracemalloc.take_snapshot()
        start_time = time.time()
        result = func(*args, **kwargs)
        snapshot_id1 = tracemalloc.take_snapshot()
        end_time = time.time()

        mem_diff = snapshot_id1.compare_to(snapshot_id0, 'lineno')
        time_data.append(end_time - start_time)
        memory_data.append(sum(block.size for block in mem_diff)/10**6)
        n_tokens.append(len(result))
        n += len(result)

        print(f"Function {func.__name__} took {end_time - start_time} seconds\n and used {sum(block.size for block in mem_diff)/10**6} MB of memory")

        if tracer_enabled:
            tracemalloc.stop()
            tracer_enabled = False

        return result
    return wrapper

def plot_complexity():
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
    res = list(nlp.pipe(docs, disable=["morphologizer", "ner", "lemmatizer", "attribute_ruler"]))
    return res

# Ne s'exécute pas dans le cas d'import de module
if __name__ == "__main__":
    input_files = glob.glob('../Corpus/*.txt') # tout les fichiers dans le dossier Corpus
    for input_file in input_files:
        process_gp2(process_gp1(preprocess_gp1(input_file)))
        print(f"Processing {input_file}...")

    print(f"Total number of tokens: {n}")
    print("Time data:", time_data)
    print("Memory data:", memory_data)

    plot_complexity()
                