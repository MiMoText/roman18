#!/usr/bin/env python3

"""
Topic Modeling with gensim: Split text in segments.
The Size of chunks is controlled by the parameter chunksize (modify in roman18_run.py).
Last chunks that are smaller than 500 words are eliminated.

"""


# == Imports == 

import os
import glob
from os.path import join
from os.path import basename
import re
import pandas as pd


# == Functions ==

def load_text(textfile):
    """
    Loads a single plain text file. 
    Provides the content as a string.
    """
    with open(textfile, "r", encoding="utf8") as infile:
        text = infile.read()
        return text


def load_metadata(metadatafile):
    """
    Loads the metadata file from disk.
    Provides it as a pandas DataFrame.
    """
    with open(metadatafile, "r", encoding="utf8") as infile:
        metadata = pd.read_csv(infile, sep=";")
        return metadata



def split_text(text, chunksize): 
    text = re.split("\W+", text)
    num_chunks = len(text) // chunksize
    chunks = [text[i:i + chunksize] for i in range(0, len(text), chunksize)]
    if len(chunks[-1]) < 500:   # last chunk is kept if >= 500 words
        chunks.pop()
    return chunks
    
    

def save_chunks(workdir, dataset, chunks, textid): 
    counter = 0
    filenames = []
    for chunk in chunks: 
        filename = textid + "_" + "{:03d}".format(counter) + ".txt"
        filepath = join(workdir, "datasets", dataset, "txt", filename)
        chunk = " ".join(chunk)
        with open(filepath, "w", encoding="utf8") as outfile:
            outfile.write(chunk) 
        filenames.append(filename)
        counter +=1
    return filenames
        
            

def write_metadata(allfilenames, metadatafile_split):
    allfilenames = pd.Series(allfilenames)
    with open(metadatafile_split, "w", encoding="utf8") as outfile: 
        allfilenames.to_csv(outfile, sep=";")



# == Coordinating function ==

def main(workdir, dataset, metadatafile_full, metadatafile_split, chunksize): 
    print("\n== splitting texts ==")
    allfilenames = []
    textpath = join(workdir, "datasets", dataset, "full", "*.txt")
    metadata = load_metadata(metadatafile_full)
    for textfile in sorted(glob.glob(textpath)):
        textid = basename(textfile).split(".")[0]
        print(textid)
        text = load_text(textfile)
        chunks = split_text(text, chunksize)
        filenames = save_chunks(workdir, dataset, chunks, textid)
        allfilenames.extend(filenames)
    write_metadata(allfilenames, metadatafile_split)
        
        
    print("== done splitting texts ==")
                       


