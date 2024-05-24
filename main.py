import spacy.tokens
from Groupe1.groupe1 import process_gp1, recursive_tokens_pos
from Groupe2.groupe2 import process_gp2
from Groupe3.groupe3 import get_annotations as process_gp3
from Groupe4.groupe4 import process_gp4
from glob import glob
from pprint import pprint
from collections import defaultdict
import sys
import spacy



def pretraitement_dico_gn(dico_gp4: dict) -> dict:
	new_dict = {}
	dico_gp4 = [dico_phrase for dico_phrase in dico_gp4 if len(dico_phrase) > 0 or (len(dico_phrase) == 1 and dico_phrase[0][0].text.strip() != "") ]
	compteur_phrase = 0
	for subdict in dico_gp4:
		new_dict.update({f"phrase_{compteur_phrase}":{}})
		tok_compteur = 0
		for i in range(len(subdict)):
			form = subdict[i][0].text
			if form.strip() != "":
				new_dict[f"phrase_{compteur_phrase}"].update({f"token_{tok_compteur}": {"form": form, "noun_phrase": subdict[i][1]}})
				tok_compteur +=1
		compteur_phrase +=1
	return new_dict




def analyse_line(line_doc: spacy.tokens.doc.Doc, dico_phrase : dict, dico_named_entites: dict, dico_noun_phrases: dict ):
	for sent in line_doc:
		liste_token = [token for token in sent]
		return get_pos(liste_token, 0, dico_phrase, dico_named_entites, dico_noun_phrases)
		

def get_pos(liste_token: list, tok_id: int, dico_phrase: dict, dico_named_entites: dict, dico_noun_phrases: dict):
	if tok_id < len(liste_token):
		token = liste_token[tok_id]
		dico_phrase.update({f"token_{tok_id}":{"form":token.text, "pos":token.pos_}})
		return get_dep(liste_token, tok_id, dico_phrase, dico_named_entites, dico_noun_phrases)
	
	else:
		return dico_phrase
	
def get_dep(liste_token: list, tok_id: int, dico_phrase: dict, dico_named_entites: dict, dico_noun_phrases: dict):
	token = liste_token[tok_id]
	dico_phrase[f"token_{tok_id}"].update({"dep": token.dep_, "head": token.head})
	return get_ne(liste_token, tok_id, dico_phrase, dico_named_entites, dico_noun_phrases)


def get_ne(liste_token, tok_id: int, dico_phrase: dict, dico_named_entites: dict, dico_noun_phrases: dict):
	if dico_phrase[f"token_{tok_id}"]["form"] == dico_named_entites[f"token_{tok_id}"]["form"]:
		dico_phrase[f"token_{tok_id}"].update({"named_entites" : dico_named_entites[f"token_{tok_id}"]["ner"]})
		return get_np(liste_token, tok_id, dico_phrase, dico_named_entites, dico_noun_phrases)
	else:
		print(tok_id)
		print(dico_phrase[f"token_{tok_id}"])
		print(dico_named_entites[f"token_{tok_id}"])
		print("erreur !")

def get_np(liste_token, tok_id: int, dico_phrase:dict, dico_named_entites: dict, dico_noun_phrases: dict):
	if dico_noun_phrases[f"token_{tok_id}"]["form"] == dico_phrase[f"token_{tok_id}"]["form"]:
		dico_phrase[f"token_{tok_id}"].update({"noun_phrase":dico_noun_phrases[f"token_{tok_id}"]["noun_phrase"]})
		return get_pos(liste_token, tok_id + 1, dico_phrase, dico_named_entites, dico_noun_phrases)
	else:
		print(dico_phrase[f"token_{tok_id}"]["form"])
		print(dico_noun_phrases[f"token_{tok_id}"]["form"])
		print("erreur !!")


def build_dico(corpus_path):
	dico = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
	dico_ne = process_gp3(corpus_path)
	for file in glob(f"{corpus_path}*.txt"):
		with open(file) as rf:
			dico_gn, cpx_gp4 = process_gp4(file)
			dico_gn = pretraitement_dico_gn(dico_gn)
			# pprint(dico_gn)
			compteur_phrases = 0
			for line in rf : 
				# print(compteur_phrases)
				line = line.strip()
				if line!= "":
					dico[file.split('/')[-1]][f"phrase_{compteur_phrases}"]["text"] = line
					# print((dico_ne[file][f"phrase_{compteur_phrases}"]))
					print(file)
					sent_doc = process_gp2(process_gp1([line]))
					for sent in sent_doc:
						dico[file.split('/')[-1]][f"phrase_{compteur_phrases}"]["tokens_decomp"].update(analyse_line([sent], {}, dico_ne[file][f"phrase_{compteur_phrases}"], dico_gn[f"phrase_{compteur_phrases}"]))
						compteur_phrases += 1
	return dico, cpx_gp4

def build_conll(dico_global: defaultdict, output_file: str)-> None:
	"""
	Inputs:
	- Dictionnaire contenant toutes les informations dont on a besoin
	- Chemin vers le fichier type conll de sortie
	Pas d'output
	"""
	with open(output_file, "w") as output:
		output.write("# global.columns = ID FORM POS HEAD DEPREL NAMED_ENTITIES NOUN_PHRASES\n")
		for file, sentence_analysis in dico_global.items():
			for sentence, analysis in sentence_analysis.items() :
				output.write(f"\n# doc_title = {file}\n# sent_id = {file.split('.')[0]}_{sentence}\n# text = {analysis["text"]}\n")
				for token, tok_analysis in analysis["tokens_decomp"].items():
					tok_id = token.split("_")[-1]
					form = tok_analysis["form"]
					pos = tok_analysis["pos"]
					head = tok_analysis["head"]
					dep = tok_analysis["dep"]
					ne = tok_analysis["named_entites"]
					gn = tok_analysis["noun_phrase"]
					output.write(f"{tok_id}\t{form}\t{pos}\t{head}\t{dep}\t{ne}\t{gn}\n")



if __name__=="__main__":
	corpus_path = sys.argv[1] if sys.argv[1][-1] == "/" else sys.argv[1] + "/"
	dico, cpx_gp4 = build_dico(corpus_path)
	# print(dico)
	build_conll(dico, sys.argv[2])
