# Grammar Checker




## Installation and Execution Instructions
- Clone the repository
- Using a terminal navigate to the "code" subdirectory (Grammars-Parsing/code as on github)
- Libraries including nltk, sklearn, csv, re, pandas, argparse should be installed
- From the terminal run the command

``` shell script
python ass2.py --input </path to file/filename.tsv> 
````
- example  
``` shell script
python main.py --input ../data/train.tsv 
```

- The train data path should be a relative path to a directory containing the text files you will use to build language models



## Resources
  - Speech and Language Processing Book by Daniel Jurafsky is used.
  - Python documentation for standard libraries


 ## Output file
 The program saves the output csv file in 
 ```
 ../output/output.tsv
```



# Grammar Checker
## Introduction
Grammar checkers like Grammarly or the one built in Microsoft Word might have helped you a lot when writing essays. In this project, you will use context-free grammars (CFG) and constituency parsing to build a very simple grammar checker. A dataset of sentences written by English learners with grammatical mistakes are provided so we can evaluate the accuracy of our grammar checker.

So how exactly does our simple grammar checker work? First of all, we have to define the set of grammar rules of English and make them machine-understandable. To be specific, we will try to come up with a very crude context-free grammar of English. After we have the CFG for English, we will run a constituency parser to parse the input sentence with that CFG. If the sentence can be successfully parsed with the CFG, we mark the input sentence as grammatically correct. And if the sentence can not be parsed, it is considered ungrammatical.

Here is an example to illustrate our grammar checker. We start with a simplified CFG that only considers the basic structure in English.



| S    -> Subj Verb Obj   | A sentence = subject + verb + object + period. |
| ------------- | ------------- |
| Subj -> NP  | The subject is a noun phrase.  |
| Obj  -> NP  | The object is also a noun phrase.  |
| NP   -> Det Noun  | A noun phrase is a determiner + a noun.  |
|   |  |
| Det  -> “the”  | The terminal symbols (lexicon) are simplified for illustration purposes.  |
| Noun -> “horse” or “apple”  |  |
| Verb -> “ate”  |  |
| .    -> “.” |  |







If we use a constituency parser (for example, the CYK algorithm) with the above CFG to parse the sentence “the horse ate the apple.”, the parsing will succeed.

But if you try the same thing with an ungrammatical sentence like “the horse ate ate the apple.”, the parser will fail. In this way, we will know that this sentence does not conform to the English grammar we defined and can call it ungrammatical.


Usually when writing grammars, one important component is the lexicon or the terminal symbols. For example, a grammar usually has a list of nouns like Noun->“horse”|“apple”. But we simplify this process by providing the part of speech tags for all input sentences. Part of speech indicates the grammatical function of a word in a sentence. For example, whether a word is a noun, adjective, verb, or a preposition. 

In this project, instead of parsing the actual sentence, we will write a grammar and a parser to parse the POS tag sequence. This will simplify the task and relieve us from building lexicons. For our above example  “The horse ate the apple.”, you will be given the POS tag sequence “DT NN VBD DT NN .”. To modify the parser to parse the POS sequence, we replace the English words in our CFG with tag names.
|  |    |
|-----|-----|
|S    -> Subj Verb Obj .| A sentence = subject + verb + object + period.| 
|Subj -> NP|The subject is a noun phrase.|
|Obj  -> NP|The object is also a noun phrase.|
|NP   -> Det Noun|A noun phrase is a determiner + a noun.|
| | |
|Det  -> “DT”|No need to put an entire English dictionary here! |
|Noun -> “NN”|   |
|Verb -> “VBD”|   |
|.    -> “.”|   |






## Tasks
Input: sentences with POS tags
The input is a tsv (tab-separated values) file like the sample:

|id|label|sentence|pos|
|--|-----|--------|---|
|73|0|Many thanks in advance for your cooperation .|JJ NNS IN NN IN PRP$ NN .| 
|74|1|At that moment we saw the bus to come .|IN DT NN PRP VBD DT NN TO VB .|


The id column is the unique id for each sentence. The label column indicates whether a sentence contains grammar errors (1 means having errors and 0 means error-free). In the sentence column, the original sentence is already tokenized and separated by a single space, so we can use the str.split() function to get the tokens. The pos column contains the POS tags for each token in the sentence, also separated by a single space. The POS tags follow the Penn Treebank (PTB) tagging scheme, as described [here](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html).
## Part 1: Building a toy grammar
The first step is to write a toy CFG for English in NLTK’s .cfg format. We can all start with this grammar below (included in the repository) and try to modify the rules or add new production rules.
|  |   |
|---|---|
|S  -> NP VP Punct|Sentence = noun phrase + verb phrase + .|
|PP -> Adp NP|Prepositional phrase = preposition + noun phrase|
|NP -> Det Noun or NP PP|Noun phrase|
|VP -> Verb NP or VP PP| Verb phrase|
|Verb -> VB \| VBD \| VBG \| VBN \| VBP \| VBZ| Include all the inflections of a verb|
|......|More production rules go here|
|Det   -> 'DT'| This part will be included in the template. See the appendix for the definitions.|
|Noun  -> 'NN'| |
|VB    -> 'VB'| |
|Adp   -> 'ADP'| |
|Punct -> 'PUNCT'| |
......



## Part 2: Constituency parsing
We use the chart parser from NLTK to parse each of the POS sequences in the dataset with the toy grammar we wrote in Part 1. The results are stored in a tsv file (not csv) with three columns:

|Column name|Description|
|-----------|-----------|
|id|The id of the input sentence.|
|ground_truth|The ground truth label of the input sentence, copied from the dataset.|
|prediction|1 if the sentence has grammar errors, 0 if not. In other words, whether the POS sequence can be parsed successfully with your grammar and parser.|


## Part 3: Evaluation and error analysis
In this part, we will evaluate the performance of our grammar checker by calculating the precision and recall of it. By looking at the output from Part 2, we are able to get the following numbers:

- TP (true positive):  the sentence contains errors and your checker found them.
- FP (false positive): the sentence is grammatical but your checker found it not.
- FN (false negative): the sentence is ungrammatical but your checker labelled it as correct.
- TN (true negative): the sentence is grammatical and your checker agrees.

The precision and recall are defined respectively as:

- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)



## TSV file
The output from Part 2 is stored in tsv format in the output/ folder.
## Grammars
The toy grammar is saved to grammars/toy.cfg. The grammars have NLTK’s .cfg format.
## Code
All the code is in the code/ folder.


## Useful links
- [Chapter 8](https://www.nltk.org/book/ch08.html) of the NLTK book introduces grammar, CFG, and constituency parsing in the context of NLTK. 
- [Chapter 12](https://web.stanford.edu/~jurafsky/slp3/12.pdf) of J+M introduces CFG and English grammar rules. [Chapter 13](https://web.stanford.edu/~jurafsky/slp3/13.pdf) covers algorithms for constituency parsing.
The PTB POS tag set is described [here](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html).
[The NLTK documentation](https://www.nltk.org) gives more details 
- Learning Objectives: Learn how to use context-free grammar to formally model constituent structures in English, and how to use a parser for constituency parsing.

## Acknowledgement
The sample toy grammar was adapted from the NLTK dataset grammars/sample/toy.cfg.


This is a solution to Assignment 2 for CMPUT 501 - Intro to NLP at the University of Alberta, created during the Fall 2020 semester.