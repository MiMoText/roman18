#!/usr/bin/env python3

"""
Doing Topic Modeling on Eighteenth-Century French Novels with gensim in the context of MiMoText:

Modeling.

Performs the main topic modeling step using the gensim library. 
This requires properly prepared forms of the corpus to be used. 

See: https://radimrehurek.com/gensim/
"""

# == Imports == 

import pickle
from os.path import join
from gensim import corpora
from gensim import models
import helpers


# == Functions ==

def build_model(dictcorpus, vectorcorpus, numtopics, passes): 
    """
    Creates the actual topic model from the data. 
    Key parameters are number of topics (numtopics) 
    and number of iterations (passes). 
    Other parameters can be set here.
    """
    model = models.ldamodel.LdaModel(
        corpus=vectorcorpus,
        id2word=dictcorpus,
        num_topics=numtopics, 
        #random_state=100,
        update_every=1000,
        chunksize=1000,
        passes=passes,
        alpha='auto',
        eta='auto',
        #minimum_probability=0.01/numtopics,
        per_word_topics=True)
    return model


# == Coordinating function ==

def main(workdir, identifier, numtopics, passes):
    print("\n== modeling ==")
    dictcorpus = helpers.load_pickle(workdir, identifier, "dictcorpus.pickle")
    vectorcorpus = helpers.load_pickle(workdir, identifier, "vectorcorpus.pickle")
    model = build_model(dictcorpus, vectorcorpus, numtopics, passes)
    helpers.save_model(workdir, identifier, model)
    print("==", helpers.get_time(), "done modeling", "==")   
    return model

