# projet groupe entités nommées

## Infos
- fin : 25/05/2024
- groupe 3: Laura et Alice
- corpus: ensemble des oeuvres de Jules Vernes [ http://abu.cnam.fr ]

## Les livrables
- un rapport détaillant la réalisation des travaux, les problèmes rencontrés, les solutions trouvées et les mesures de complexité
- le code attendu pour le module ou l'infrastructure de la chaîne en fonction du module traité par l'équipe
- une copie du corpus avant-après l'étape de traitement

## partie 1: les entités nommées
- spécifier et implémenter une chaîne de traitement en python pour réaliser une fonction d'extraction (**extraction des entités nommées**) dans un corpus français.
=> faire choix (argumenté) d'une technologie pertinente en fonction de votre objectif et de vos moyens (compétence, charge de travail et moyens informatiques): spacyyyyyyyyyyyyy
=> faire description des données d'entrées, des données de sortie et de la fonction réalisée sur ces données au moyen de fonctions récursives abstraites; vos fonctions ne coderont que les paramètres d'entrée et une description récursive utilisant des fonctions qui vous serviront à expliciter les étapes du traitement, mais pour lesquel vous ne donnerez que le nom et la liste des paramètres, sans en coder le corps (en gros, pas besoin de tout coder une chaine complète fonctionnelle)

## partie 2: la complexité théorique
- mesurerez  la complexité théorique empirique moyenne en temps et en espace de chaque chaque module, et vous proposerez si cela est possible une confirmation de vos mesures pour les différents modules en vous appuyant sur une recherche bibliographique.

## exemple pour la spécification au moyen de fonction récursives

Si par exemple je veus spécifier un tokenizer à partir de fonctions récursives de lecture de caractères individuels afin de traiter une liste de fichier, je pourrais écrire ceci. 
Nous pourrions nous arrêter pour une sepification abstraite sans définir les fonctions qui manquent, à savoir les quatre fonctions : eof(), open_file_lecture(), close_file() et read_1_char()
Si vous voulez obtenir une simulation exécutable à partir de votre définition abstraite en fonctions récursive, il vous suffit d'implémenter à minima ces quatres fonctions restantes de façon à faire tourner votre tokenizer sur un exemple "jouet".

```python

def my_tokenizer( file_lst == [], charset == [] ):
   if file_lst == []
      return []
   else:
      return file_tokenizer( file_lst[ 0 ], charset ) +  my_tokenizer( file_lst[ 1: ], charset )

def file_tokenizer( file_nm = "", charset ):
    return file_postprocess( file_process( file_preprocess( file_nm ), charset ) )

def file_preprocess( file_nm = "" ) 
    return open_file_lecture( file_nm )

def file_process( file_desc, charset, tokens = [] ):
    if eof( file_desc ):
       return tokens
    else:
       # notez qu'ici get_next_token() va faire un effet de bord (changement de valeur
       # du pointeur de début) sur file_desc en lisant le token suivant.
       return file_process( file_desc, tokens + [ get_next_token( file_desc, charset ) ] )

def file_postprocess( file_desc, charset = [], tokens = [] ):
    close_file( file_desc )
    return tokens

def get_next_token( file_desc, charset, tok = '' ):
    if eof( file_desc ):
       return tork
    else:
       # notez qu'ici read_1_char() va faire un effet de bord (changement de valeur
       # du pointeur de début) sur file_desc en lisant le caractère suivant.	
       return get_next_token( file_desc, tok + read_1_char( file_desc ) )
```
