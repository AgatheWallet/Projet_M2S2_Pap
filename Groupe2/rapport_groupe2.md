## Rapport du Groupe 2: Analyse syntaxique en dépendances
**Auteurs**: Liza FRETEL, Kenza AHMIA, Shami THIRION SEN

### Introduction
Dans le cadre du projet de l'implémentation d'une chaîne de traitement pour analyse du langage naturel en Python pour réaliser l'extraction des caractéristiques linguistique d'un corpus littéraire (?), les différentes tâches ont été divisés parmi les étudiants en M2. Le groupe 2 s'est chargé de **l'analyse syntaxique en dépendances** (module 2). Notre travail a consisté à assurer la continuité du flux de données entre les modules, à ajouter des couches d'analyse supplémentaires, et à mesurer la complexité en termes de temps et d'espace pour optimiser les performances globales du système.

### Le chemin

`sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Groupe1')))` permet d'ajouter un chemin  vers le répertoire Groupe1. De cette façon, nous pouvons importer `process_gp1` et `preprocess_gp1` depuis le module du groupe1 depuis le repertoire Groupe1. Ces fonctions sont ainsi utilisées dans notre script pour effectuer des prétraitements et des traitements sur les données textuelles. En important uniquement ces fonctions, le script ne charge que ce qui est nécessaire, ce qui peut améliorer l'efficacité et la lisibilité du code. [`LIZA` comments??]

### Les fonctions

Nous implémentons 3 fonctions principales: 
- `process_gp2(docs)`
-  `time_and_memory_wrapper(func)`
-  `plot_complexity()`
  
Les fonctions sont évaluées en termes de temps d'exécution et d'utilisation de la mémoire, afin d'identifier les éventuels goulots d'étranglement et d'optimiser le processus de traitement.

### `process_gp2(docs)`
`process_gp2` est la fonction principale pour l'analyse syntaxique en dépendance. Elle utilise le pipeline NLP de SpaCy. Elle prend en entrée une liste de documents textuels et retourne une liste de tuples contenant des informations sur chaque token traité. Cette fonction est enveloppée par le décorateur `time_and_memory_wrapper`, ce qui permet de mesurer les performances de traitement. En évaluant cette fonction, on peut obtenir des informations sur les performances spécifiques du pipeline NLP utilisé, ce qui est crucial pour l'optimisation du système dans son ensemble.

### `time_and_memory_wrapper(func)`
La fonction `time_and_memory_wrapper` est un décorateur qui permet de mesurer le temps d'exécution et la mémoire utilisée par une fonction donnée. En enveloppant une fonction avec ce décorateur, on obtient des informations  sur les performances à chaque éxecution. Le décorateur utilise le module `tracemalloc` pour mesurer la mémoire utilisée avant et après l'exécution de la fonction, et le module `time` pour mesurer le temps écoulé. Les résultats sont ensuite stockés dans les listes globales `time_data` et `memory_data`, permettant l'analyse, l'import et la visualisation ultérieurs.

#### [Liza] tu peux rajouter qqs lignes pour la fonction, pour expliquer la continuité du groupe 1 et comment ça sert les groupe 4  stp?

### `plot_complexity()`
`plot_complexity` génère un graphique représentant l'évolution de la complexité en fonction du nombre de tokens. Elle utilise les données collectées sur le nombre de tokens, le temps d'exécution et la mémoire utilisée pour chaque exécution de fonction. Ce graphique permet une visualisation claire des tendances de performance du en fonction de la charge de traitement. Les axes x et y représentent respectivement le nombre de tokens et le temps d'exécution et la mémoire utilisée. Cette fonction est essentielle pour détecter les éventuels déficience pour optimiser les performances globales du système.

### Le script
Le script `groupe2.py` peut être appelé de 2 façons: 
- depuis le terminal: afin d'effectuer l'analyse syntaxique et d'examiner la taille du corpus et les compléxités en temps et en mémoire pour chaque fichier. 
- via l'import des modules par d'autres groupes afin d'assurer la continuité dans la chaîne de traitement `LIZA`(si tu veux bien ajouter qqs lignes de plus , pretty please)


### Les défis rencontrés
Contrairement, au projet réalisé lors du 1er semestre, pour le projet actuel nous n'avons pas réussi à organiser une réunion préparatoire afin de commencer les étapes. Comme nous pouvions le deviner, ceci a généré quelques malentendus concernant la chaîne de traitement et la structure de sortie attendus par les groupes suivants. Néanmoins, nous avons réussi à nous organiser avec les groupes précédent et suivant, afin que que les modules soient exploitables, sans «casser» la chaîne de traitement.


## Conclusion

[je refais la conclsion selon les modif - 1 paragraphe ou 2 max.]

Ce rapport présente une analyse approfondie des performances des fonctions de traitement NLP, en mettant l'accent sur la mesure du temps d'exécution et de l'utilisation de la mémoire. En utilisant des outils de mesure appropriés et des visualisations graphiques, nous avons pu identifier les zones d'amélioration potentielles et guider le processus d'optimisation du système NLP. Ces informations sont essentielles pour assurer des performances optimales dans des environnements de traitement de texte à grande échelle.


