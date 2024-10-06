# -*- coding: utf-8 -*-
"""
word2vec embeddings start with a line with the number of lines (tokens?) and 
the number of dimensions of the file. This allows gensim to allocate memory 
accordingly for querying the model. Larger dimensions mean larger memory is 
held captive. Accordingly, this line has to be inserted into the GloVe 
embeddings file.
"""

import os
import shutil
import smart_open
from sys import platform

import gensim

# Input: GloVe Model File
# More models can be downloaded from http://nlp.stanford.edu/projects/glove/
#glove_file="glove.6B.300d.txt"
glove_file=r'glove.42B.300d.txt'



# Output: Gensim Model text format.
gensim_file='glove_model2.txt'


# Demo: Loads the newly created glove_model.txt into gensim API.


model=gensim.models.KeyedVectors.load_word2vec_format(gensim_file,binary=False) #GloVe Model

# word="cry"
# word=word.lower()
# print(model.most_similar(positive=[word], topn=20))

print("In Vector Model")

def get_vector(word):
    word=word.lower()
    try:
        print("got vector")
        print(word)
        return model[word]
    except:
        print("no vector")
        return None

def get_similarity(vector):
    sim=model.similar_by_vector(vector, topn=11, restrict_vocab=None)
    return sim
