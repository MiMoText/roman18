#!/usr/bin/env python3

"""
Doing Topic Modeling on Eighteenth-Century French Novels with gensim in the context of MiMoText:

Overview visualization.

Using the pyLDAvis library, provides an interactive overview 
visualisation of the topic model.

See: https://pyldavis.readthedocs.io/en/latest/
"""

from os.path import join
import pyLDAvis
import pyLDAvis.gensim
import helpers


def visualize_model(model, dictcorpus, vectorcorpus, vizfile):
    visualization = pyLDAvis.gensim.prepare(model, vectorcorpus, dictcorpus, sort_topics=False, mds="mmds")
    pyLDAvis.save_html(visualization, vizfile)


def main(workdir, identifier):
    print("\n== visualize_model ==")
    model = helpers.load_model(workdir, identifier)
    vizfile = join(workdir, "results", identifier, "visualization.html")
    dictcorpus = helpers.load_pickle(workdir, identifier, "dictcorpus.pickle")
    vectorcorpus = helpers.load_pickle(workdir, identifier, "vectorcorpus.pickle")
    visualize_model(model, dictcorpus, vectorcorpus, vizfile)
    print("==", helpers.get_time(), "done visualizing", "==")   
