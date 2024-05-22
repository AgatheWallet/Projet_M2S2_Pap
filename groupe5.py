from Groupe1.groupe1 import preprocess_gp1, process_gp1
from Groupe2.groupe2 import process_gp2
from collections import defaultdict
from pprint import pprint
from glob import glob
import sys


if __name__ == "__main__":
	dico_global = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

	for fichier in glob(f"{sys.argv[1]}*.txt"):
		compteur_sent = 0
		for phrase in process_gp2(process_gp1(preprocess_gp1(fichier))):
			if len(phrase) > 0:
				# print(phrase, compteur_sent)
				compteur_tok = 0
				for tok in phrase:
					dico_global[fichier.split('/')[-1]][f"phrase_{compteur_sent}"][f"token_{compteur_tok}"] = {"form":tok.text,"pos" : tok.pos_, "dep": tok.dep_, "head":tok.head}
					compteur_tok += 1
				compteur_sent += 1
	pprint(dico_global)