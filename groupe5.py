from Groupe1.groupe1 import preprocess_gp1, process_gp1
from Groupe2.groupe2 import process_gp2
from Groupe3.groupe3 import get_annotations
from Groupe4.groupe4 import process_gp4
from collections import defaultdict
from pprint import pprint
from glob import glob
import sys


def get_pos_dep(corpus: str, dico_global: defaultdict) -> defaultdict:
	for fichier in glob(f"{corpus}*.txt"):
		compteur_sent = 0
		for phrase in process_gp2(process_gp1(preprocess_gp1(fichier))):
			if len(phrase) > 0:
				# print(phrase, compteur_sent)
				compteur_tok = 0
				dico_global[fichier.split('/')[-1]][f"phrase_{compteur_sent}"]["text"] = phrase.text.strip()
				for tok in phrase:
					dico_global[fichier.split('/')[-1]][f"phrase_{compteur_sent}"]["tokens_decomp"][f"token_{compteur_tok}"] = {"form":tok.text,"pos" : tok.pos_, "dep": tok.dep_, "head":tok.head}
					compteur_tok += 1
				compteur_sent += 1
	return dico_global

def get_named_entities(corpus: str, dico_global: defaultdict) -> defaultdict:
	dico_groupe3 = get_annotations(corpus)
	for fichier, dico_phrase in dico_groupe3.items():
		for phrase_id, token_dec in dico_phrase.items():
			for tok_id, analyse in token_dec.items():
				if analyse['form'] == dico_global[fichier.split('/')[-1]][phrase_id]["tokens_decomp"][tok_id]["form"]:
					dico_global[fichier.split('/')[-1]][phrase_id]["tokens_decomp"][tok_id].update({"ner":analyse["ner"]})
				else:
					print("erreur !")
	return dico_global


def get_nominal_syntagms(corpus: str, dico_global: defaultdict) -> defaultdict:
	pass
		


if __name__ == "__main__":
	dico = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
	corpus_path = sys.argv[1] if sys.argv[1][-1] == "/" else sys.argv[1] + "/"
	dico = get_pos_dep(corpus_path, dico)
	dico = get_named_entities(corpus_path, dico)
	pprint(dico)