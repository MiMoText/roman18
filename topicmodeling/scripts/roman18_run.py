#!/usr/bin/env python3

"""
Doing Topic Modeling on Eighteenth-Century French Novels with gensim in the context of MiMoText.

This is the main coordination script.
It allows you to set the pipeline parameters.
It allows you to determine which components will be run. 

Calling:
- split_texts: splitting novel files into smaller chunks of text
- roman18_preprocessing: lemmatizing, POS-tagging and filtering

To be continued.
"""


# == Imports ==


from os.path import join

import helpers
import roman18_split
import roman18_preprocessing


# == Files and folders ==

workdir = ".."            
dataset = "roman18-test"             
identifier = "rom18-test"

metadatafile_full = join(workdir, "datasets", dataset, "metadata-full.csv")
metadatafile_split = join(workdir, "datasets", dataset, "metadata.csv")
stoplistfile = "fr.txt"


# == Parameters ==

chunksize = 1000
lang = "presto"   # possible values: "fr" (standard French); "presto" (French of the 16th and 17th century)

# == Coordinating function ==

def main(workdir, dataset, identifier, lang, metadatafile_full, metadatafile_split, stoplistfile, chunksize):
    print("==", "starting", "==", "\n==", helpers.get_time(), "==")
    helpers.make_dirs(workdir, identifier)
    roman18_split.main(workdir, dataset, metadatafile_full, metadatafile_split, chunksize)
    roman18_preprocessing.main(workdir, dataset, identifier, lang, stoplistfile)
    print("\n==", helpers.get_time(), "done", "==")

    
main(workdir, dataset, identifier, lang, metadatafile_full, metadatafile_split, stoplistfile, chunksize)

