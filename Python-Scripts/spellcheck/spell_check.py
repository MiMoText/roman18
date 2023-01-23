
"""
@author: Ulrike Henny, Christof Schöch

Submodule for checking the orthography of a text collection. The expected input are plain text files.

To install further dictionaries: sudo apt-get install myspell-es (etc.)
See http://pythonhosted.org/pyenchant/ for more information about the spellchecking library used
Information on installing and storing the required dictionary files:
https://pyenchant.github.io/pyenchant/install.html#installing-a-dictionary
"""


# =======================
# Imports
# =======================


import enchant
from enchant import checker
from enchant.tokenize import get_tokenizer
import collections
import pandas as pd
import os
import glob
import sys
import re
import csv
from os.path import join


# =======================
# Files and folders
# =======================


wdir = ""
inpath = join(wdir, "plain", "files", "*.txt")
outpath = join(wdir, "plain", "spellcheck.csv")
lang = "fr"
wordFiles = ""


# =======================
# Functions
# =======================


def check_collection(inpath, outpath, lang, wordFiles=[]):
    """
    Checks the orthography of the text in a collection. The expected input are plain text files.
    
    Arguments:
    inpath (string): path to the input files, including file name pattern
    outpath (string): path to the output file, including the output file's name
    lang (string): which dictionary to use, e.g. "es", "fr", "de"
    wordFiles (list): optional; list of strings; paths to files with lists of words which will not be treated as errors (e.g. named entities)
    """

    try:
        enchant.dict_exists(lang)
        try:
            tknzr = get_tokenizer(lang)
        except enchant.errors.TokenizerNotFoundError:    
            tknzr = get_tokenizer()
        chk = checker.SpellChecker(lang, tokenize=tknzr)
        
    except enchant.errors.DictNotFoundError:
        print("ERROR: The dictionary " + lang + "doesn't exist. Please choose another dictionary.")
        sys.exit(0)

    all_words = []
    all_num = []
    all_idnos = []

    print("...checking...")
    for file in glob.glob(inpath):
        idno,ext = os.path.basename(file).split(".")
        all_idnos.append(idno)
        
        err_words = []

        with open(file, "r", encoding="UTF-8") as fin:
            intext = fin.read().lower()
            chk.set_text(intext)

        if len(wordFiles) !=0:
            allCorrects = ""
            for file in wordFiles:
                with open(file, "r", encoding="UTF-8") as f:
                     corrects = f.read().lower()
                     allCorrects = allCorrects + corrects

        for err in chk:
            if not wordFiles or err.word not in allCorrects: 
                err_words.append(err.word)
            all_words.append(err_words)

        err_num = collections.Counter(err_words)
        all_num.append(err_num)
        
        print("..." + str(len(err_num)) + " different errors found in " + idno)
        
    df = pd.DataFrame(all_num,index=all_idnos).T
    
    df = df.fillna(0)
    df = df.astype(int)
    
    df["sum"] = df.sum(axis=1)
    # df = df.sort("sum", ascending=False)
    df = df.sort_values(by="sum", ascending=False)
    
    df.to_csv(outpath)
    print("done")



# =======================
# Main
# =======================


def main(inpath, outpath, lang, wordFiles):
    check_collection(inpath, outpath, lang, wordFiles)  

main(inpath, outpath, lang, wordFiles)

