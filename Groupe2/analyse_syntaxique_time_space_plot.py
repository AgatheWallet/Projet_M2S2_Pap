import spacy
import time
import tracemalloc
import matplotlib.pyplot as plt
import glob

tracer_enabled = False
time_data = [] # temps d'exécution
memory_data = [] # mémoire utilisée
n = 0 # nombre de tokens

def time_and_memory_wrapper(func):
    def wrapper(*args, **kwargs):
        global tracer_enabled, n, time_data, memory_data
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
        n += len(result)

        print(f"Function {func.__name__} took {end_time - start_time} seconds\n and used {sum(block.size for block in mem_diff)/10**6} MB of memory")

        if tracer_enabled:
            tracemalloc.stop()
            tracer_enabled = False

        return result
    return wrapper

def plot_complexity():
    plt.figure(figsize=(10, 6))
    plt.plot(time_data, label='Time (actual)')
    plt.plot([n*10 for n in range(len(time_data))], label='Time (theoretical)')
    plt.plot(memory_data, label='Memory (actual)')
    plt.plot([n*10 for n in range(len(memory_data))], label='Memory (theoretical)')
    plt.xlabel('Number of tokens')
    plt.ylabel('Time (s) / Memory (MB)')
    plt.legend()
    plt.grid()
    plt.savefig('complexity.png')
    plt.pause(15)
    plt.close('all')
    plt.show()

nlp = spacy.load("fr_core_news_sm")

@time_and_memory_wrapper
def preprocess_gp1(inputFile):
    with open(inputFile, 'r') as file:
        textes = file.readlines()
    return textes

@time_and_memory_wrapper
def process_gp1(textes):
    res = list(nlp.pipe(textes, disable=["parser", "ner", "lemmatizer", "attribute_ruler"]))
    return res

@time_and_memory_wrapper
def process_gp2(docs):
    res = list(nlp.pipe(docs, disable=["morphologizer", "ner", "lemmatizer", "attribute_ruler"]))
    return res


# input_file = '../Groupe1/petit_test.txt' # test avec fichier de petit_test.txt 


input_files = glob.glob('../Corpus/*.txt') # tout les fichiers dans le dossier Corpus
for input_file in input_files:
    process_gp2(process_gp1(preprocess_gp1(input_file)))
    print(f"Processing {input_file}...")

print(f"Total number of tokens: {n}")
print("Time data:", time_data)
print("Memory data:", memory_data)

plot_complexity()
