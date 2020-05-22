#!/usr/bin/env python3

"""
Topic Modeling with gensim: helper functions.

This module provides some helper functions used by various other modules.
"""

import os
import pickle
from os.path import join
from gensim import models
from datetime import datetime



def make_dirs(workdir, identifier):
    """
    Creates the folders required by the subsequent modules.
    """
    picklesfolder = join(workdir, "results", identifier, "pickles", "")
    if not os.path.exists(picklesfolder):
        os.makedirs(picklesfolder)
    modelsfolder = join(workdir, "results", identifier, "model", "")
    if not os.path.exists(modelsfolder):
        os.makedirs(modelsfolder)
    wordcloudsfolder = join(workdir, "results", identifier, "wordles", "")
    if not os.path.exists(wordcloudsfolder):
        os.makedirs(wordcloudsfolder)


def save_pickle(data, workdir, identifier, picklename):
    """
    Save any intermediary data to the Python binary file format for retrieval later on.
    """
    picklesfile = join(workdir, "results", identifier, "pickles", picklename)
    with open(picklesfile, "wb") as filehandle:
        pickle.dump(data, filehandle)


def load_pickle(workdir, identifier, picklename):
    """
    Load any intermediary data from a previous step for further processing.
    """
    picklesfile = join(workdir, "results", identifier, "pickles", picklename)
    with open(picklesfile, "rb") as filehandle:
        data = pickle.load(filehandle)
        return data


def save_model(workdir, identifier, model):
    """
    Save a gensim model to file for later use.
    """
    modelfile = join(workdir, "results", identifier, "model", identifier+".gensim")
    model.save(modelfile)


def load_model(workdir, identifier): 
    """
    Load a gensim model file for further processing.
    """
    modelfile = join(workdir, "results", identifier, "model", identifier+".gensim")
    model = models.LdaModel.load(modelfile)
    return model


def get_time(): 
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

