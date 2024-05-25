# Rapport Groupe 3 - Extraction des entités nommées

Notre tâche a été de créer un module qui prend en entrée un corpus de textes et fournit en sortie les données annotées en entitées nommées. Ce module et sa sortie ont été conçus pour pouvoir s'insérer dans une chaîne de traitement en quatre étapes : étiquetage morpho-syntaxique (M1), analyse syntaxique en dépendances (M2), **extraction des entitées nommées (M3)**, et extraction des groupes nominaux (M4).

## I. Présentation des données et du modèle

### Le choix du module Spacy

Il a été choisi en accord avec les autres groupes. En effet, puisque la chaîne de traitement était divisée en quatre tâches, nous avons décidé ensemble de l'utiliser car il permet de rassembler les différentes tâches dans un seul objet : le SpacyDoc.

<img title="schema d'un doc spacy" src="https://github.com/AgatheWallet/Projet_M2S2_Pap/blob/main/Groupe3/images/SpacyDoc.png" alt="" align="center">

### La tâche de reconnaissance des entités nommées (NER)

Une entité nommée est de manière globale tout mot forme qui pourrait être assimilé à un nom propre : les noms de personnes ou d'organisations, les sociétés, les noms de lieux, de pays, les États, les noms des œuvres, etc.

Contrairement aux tâches d'étiquetage en parties du dicours ou de lemmatisation qui octroient une étiquette par token, la reconnaissance des entités nommées cherche à identifier un token ou souvent un empan, une séquence de tokens (span), pour l'étiqueter. La reconnaissance d'EN du modèle Spacy est donc une fonctionnalité pré-entraînée. La composante `ner` du modèle utilise sa propre couche de vecteurs (tok2vec) afin de prédire les EN. Vous pouvez retrouver des informations supplémentaire dans la [documentation spacy](https://spacy.io/api/entityrecognizer).

L'entraînement du modèle de reconnaissance des EN de Sapcy a été réalisé avec les données wikipedia du corpus [*Wikiner*](https://figshare.com/articles/dataset/Learning_multilingual_named_entity_recognition_from_Wikipedia/5462500).

#### L'annotation BIO

On peut récupérer, à partir du token d'un objet SpacyDoc, les informations suivantes : 
- la forme : *token*.text
- l'étiquette IOB : *token*.ent_iob_
- le type d'EN, soit l'étiquette : *token*.ent_type_

Le modèle Spacy utilise l'**annotation BIO**. Celle-ci associe une étiquette à chaque token. Cette étiquette est la lettre 'O' (pour "Outside") si le token n'est pas reconnu comme une EN. S'il est reconnu comme étant une EN, la lettre 'B' (pour "Beginning") lui est associée. Si l'entité nommée reconnue est composée de plusieurs tokens, le ou les tokens suivants appartenant à la même entitée seront étiquetés avec la lettre 'I' (pour "Inside").

Le SpacyDoc est créé et implémenté avec l'appel du modèle Spacy et l'affectation de son résultat à la variable docs : 

```python
docs = list(nlp.pipe(texte, disable=["parser", "lemmatizer", "attribute_ruler"]))
```

La variable docs est une liste de SpacyDoc (spacy.tokens.doc.Doc). Chaque élément de la liste correspond à une phrase segmentée en Token selon la formulation de Spacy (cf. [schéma SpacyDoc](https://github.com/AgatheWallet/Projet_M2S2_Pap/blob/main/Groupe3/rapport_groupe3.md#le-choix-du-module-spacy)).

### Le choix du calcul de complexité

Le script du Groupe 5 qui est en charge d'intégrer les différentes modules, prend la sortie de notre script : `from Groupe3.groupe3 import get_complexities`

La fonction `get_complexities() `retourne une liste de 4 listes, dont les 3 premières seront utilisées afin qu'il puisse calculer la complexité moyenne en temps et en espace de chaque module : 
- la liste du nombre de tokens par texte
- la liste du temps d'exécution en sec par texte
- la liste des compteurs de la complexité empirique en espace mémoire. 

Nous avons un compteur supplémentaire qui calcule le nombre d'appels de fonction pendant l'execution, une métrique qui nous a paru intéressante pour notre programme récursif. 

### La construction des dictionnaires

Nous avons récupéré pour chaque token son étiquette : I, B ou O, et son label (`.ent_type_` : le type de l'entité nommée) s'il en a un. Le format du dictionnaire a été fait selon les demandes du groupe 5 pour permettre une extraction facile des labels des entités nommés. Il suit les règles suivantes :

```python
  {
    "nom_du_fichier" : {
      "phrase_n" : {
        "token_n" : {
          "form" : token.text,
          "ner" : "O"
        },
        "token_n+1" : {
          "form" : token.text,
          "ner" : token.ent_iob+"-"+token.ent_type_
        }
      }
    }
  }
```

L'annotation a été effectuée token par token. Spacy propose également une sortie qui regroupe les tokens, mais cette sortie ne s'accordait pas avec celles des autres modules de la chaîne de traitement.

## II. Le module

```mermaid
flowchart TD

subgraph "Création du dictionnaire final et enregistrement des annotations au format json"
  A(get_annotations) ----> O[boucle for pour travailler fichier par fichier]
  O -- "appelle" --> B(preprocess_file)

  subgraph "Transformation du fichier en liste de lignes et analyse avec spaCy"
    B -- "appelle" --> C(analyse_spacy)
    C -- "appelle" --> D(process_file)

    subgraph "Création du dictionnaire"
      D -- "appelle" --> E(process_line)
      D -- "boucle tant qu'il reste des lignes à annoter" --> D
      E -- "boucle tant qu'il reste des tokens à annoter" --> E
    end
  end

  A -- "renvoie dictionnaire" --> F(main)
  F -- "enregistre dans" --> G{annotations_EN.json}
end
```

Il n'y a pas eu de problèmes particulièrement compliqués pendant l'écriture du fichier ou l'intégration des compteurs. Le groupe 5 nous a fait remarquer qu'il y avait des tokens vides annotés dans notre sortie. En fait, Spacy comptait comme token tout endroit où plusieurs espaces de succédaient. Un simple nettoyage du texte a suffit à résoudre ce problème. 

## III. La compléxité empirique du module en temps et en espace

| corpus               | nb tokens | espace (nb éléments) | temps (sec.) | temps (nb appels) |
| -------------------- | --------- | -------------------- | ------------ | ----------------- |
| JV-Terre_Lune        | 66352     | 68107                | 21.422       | 68969             |
| JV-Revoltes_Bounty   | 8266      | 8708                 | 2.138        | 8585              |
| JV-5_semaines_ballon | 98817     | 102264               | 41.154       | 104494            |
| JV-Tour_monde        | 86349     | 88928                | 31.189       | 90822             |
| JV-Forceurs_blocus   | 23525     | 24606                | 6.646        | 24932             |
| JV-Robur             | 73354     | 75576                | 25.532       | 76601             |
| JV-Begum             | 64440     | 66132                | 19.266       | 66949             |

On peut déjà observer avec notre petit corpus de 7 textes que les ordres de grandeurs des variables du calcul de complexité sont similaires.

### Complexité empirique en espace

La complexité empirique en espace mémoire est calculée à partir du nombre d'éléments de toutes les séquences, tous les dictionnaires et les SpacyDoc. L'idée est de compter les éléments par fichier texte et de garder la valeur la plus grande du décompte.

Le nombre des éléments pris en compte est représentés par les len() et les sum() suivants :

- dans *def preprocess_file()* : `len(texte)` le nombre des phrases dans un texte
- dans *def analyse_spacy()* : `sum([len(doc) for doc in docs])` la somme du nombre de Token de chaque chaque SpacyDoc.
- dans *def process_file()* : `(len(dicos) + len(docs)-1) + sum([len(doc) for doc in docs]) + sum([1 for dico in dicos for token in dico.keys()])` : le nombre de dictionnaires, le nombre de SpacyDoc

### Complexité empirique en temps

###### Au moyen du module Python *time*

On calcule le temps d'exécution des cinq fonctions du script, donc pour le traitement d'un fichier.

S'il est réitéré, le calcul ne renvoie jamais la même mesure, le temps d'exécution est influencé par le nombre de tâches en arrière-plan dans la machine et il peut  donner pour un même script et pour les mêmes données, un résultat différent selon le système d'exploitation, la machine etc.

Compte tenu du fait que nos fonctions sont récursives, il est intéressant de se concentrer sur le nombre d'appels de fonctions pour mesurer la complexité en temps. C'est ce que nous avons fait en incrémentant un compteur dans l'appel de la fonction dans le return.

La tendance de la courbe des plots est quasi-linéaire, cela nous laisse penser que l'on a une complexité empirique de l'ordre de O(N).
