'''
The script produces a CSV of word forms that are new candidates
for historical word forms to be modernized.

This script takes the current modernization list (modlist),
the new Spellcheck output (e.g. after expanding the novelcollection),
and an existing name list (containing already sorted out proper names).

The threshold defines the minimum number of times the word form
should occur in the corpus.

'''

#==============
# Imports 
#==============

import os.path
import glob
from os.path import join
from lxml import etree
import pandas as pd
import re
import csv


# =======================
# Files and folders
# =======================


wdir = ""
modlist = join(wdir, "modlist_final.csv")  # current modernization list
spellcheckfile = join(wdir, "spellcheck.csv")  # new ppellcheck output
namelist = join(wdir, "names.txt")  # name list (containing already sorted out proper names)
outpath = join(wdir, "modlist_ext.csv")  # Output: Liste erweitert mit neuen zu modernisierenden Formen

treshold = 5   # Threshold for the selection of word forms to be modernized


#==============
# Functions 
#==============


def get_spellchecklist(spellcheckfile, treshold):
    '''
    Input: CSV-Tabelle mit allen von spellcheck.py entdeckten "Fehlern" + Schwellwert (erstellt mit kompletter Textsammlung inkl. neuer Romane)
    ! In Wortverbindungen mit verkürzten, apostrophierten Wörtern (z.B. j'avois) wird der erste Teil getilgt.
    Output: Liste mit Wörtern, die mindestens so oft vorkommen, wie im Parameter treshold angegeben
    
    '''
    errors = []
    abbrlist = ["j'", "n'", "l'", "s'", "m'", "t'", "c'", "d'"]
    with open(spellcheckfile, "r", encoding="utf8", newline="\n") as infile: 
        spells = pd.read_csv(infile, delimiter=",")
        spells = spells.rename(columns={'Unnamed: 0': 'misspelled'})
        for ind in spells.index:
            if spells.loc[ind, 'sum'] > treshold-1:   # treshold 
                error = spells.loc[ind, 'misspelled']
                if error[:2] in abbrlist:
                    error = error[2:]
                    errors.append(error)
                else:
                    errors.append(error)       
    return errors
    
    
def get_modlist(modlist):
    '''
    Input: CSV with all words and modernized forms of the current modernization list (without the proper names).
    Output: List of original (non-modernized) words
    
    '''
    with open(modlist, "r", encoding="utf8", newline="\n") as infile: 
        mods = csv.reader(infile, delimiter=",")
        mod_words = []
        for row in mods:
            parts = row[0].split("=")
            mod_words.append(parts[0])
        return mod_words
    
    
def get_namelist(namelist):
    '''
    Input: TXT file with names that have already been sorted out
    Output: List with these names
    '''
    names = []
    with open(namelist, "r", encoding="utf8") as infile: 
        text = infile.read()
        lines = text.split("\n")
        for line in lines:
            names.append(line)
    return names


def append_modlist(modlist, errors, mod_words, names):
    '''
    Any word in the spellcheck list (errors) that is not already in the current
    modernization list (mod_words) nor in the name list is added to the mod_append list
    (in the form [word, word]). This list is converted to a dataframe.
    (The second word form has to replaced manually by the modern word form.)
    '''
    mod_append = []
    for word in errors:
        if word not in mod_words and word not in names:
            mod_append.append([word, word])
    append_df = pd.DataFrame(mod_append, columns = ['original', 'modernisé'])
    return append_df
    



def save_modlist(append_df, outpath):
    append_df.to_csv(outpath)
    
            
# == Coordinating function ==

def main(spellcheckfile, treshold, modlist, namelist, outpath): 

    errors = get_spellchecklist(spellcheckfile, treshold)
    mod_words = get_modlist(modlist)
    names = get_namelist(namelist)
    append_df = append_modlist(modlist, errors, mod_words, names)
    save_modlist(append_df, outpath)
    
main(spellcheckfile, treshold, modlist, namelist, outpath)
