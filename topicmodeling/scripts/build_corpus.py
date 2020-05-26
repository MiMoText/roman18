#!/usr/bin/env python3

"""
Doing Topic Modeling on Eighteenth-Century French Novels with gensim in the context of MiMoText.

"""


import os
import glob
import pickle
from os.path import join
from os.path import basename
from collections import defaultdict
from gensim import corpora
import helpers


      
def build_vectorcorpus(allprepared):
    dictcorpus = corpora.Dictionary(allprepared)
    vectorcorpus = [dictcorpus.doc2bow(text) for text in allprepared]
    print("number of types in corpus:", len(dictcorpus))
    return dictcorpus, vectorcorpus



def main(workdir, identifier):
    print("\n== text2corpus ==")
    allprepared = helpers.load_pickle(workdir, identifier, "allprepared.pickle")
    dictcorpus, vectorcorpus = build_vectorcorpus(allprepared)
    helpers.save_pickle(dictcorpus, workdir, identifier, "dictcorpus.pickle")
    helpers.save_pickle(vectorcorpus, workdir, identifier, "vectorcorpus.pickle")
    print("==", helpers.get_time(), "done building corpus", "==")   

