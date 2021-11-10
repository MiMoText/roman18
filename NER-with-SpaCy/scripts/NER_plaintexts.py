#!/usr/bin/env python3

'''
NER_plaintexts.py

Parse a directory of plain text files, find named entities
with spaCy, and store the results in a .csv table.
'''

from collections import Counter
from functools import reduce
from glob import glob
import logging
from pathlib import Path

import pandas as pd
import spacy

# Adjust the following config variables as needed.
# The directory where the plain text files are stored, and where
# the eventual results should be stored.
PLAIN_TEXT_DIR = '../../plain/files/'
RESULT_FILE_PATH = 'ner_loc_per.csv'

# On machines with limited memory, some of the larger
# documents might cause OOM. To prevent that, it is
# possible to split the texts into chunks of the given
# word count. Set to `None` to disable chunking.
CHUNK_SIZE = 120_000

# spaCy uses a maximum text length (in characters) for
# at document creation to prevent OOM. The default
# is 1_000_000. If `CHUNK_SIZE` is used, it will probably
# prevent the docs from ever reaching this size.
MAX_DOC_LENGTH = 2_000_000 

# Reload the spaCy language model every N iterations.
# Drastically increases runtime, but can save a bit of
# memory because it also clears spaCy's internal String
# Store. Set to `None` to disable model reloading.
# Since this should not normally be our bottleneck, the
# default setting is `None`.
RELOAD_MODEL = None

# The number of most frequent NEs to store.
MOST_FREQUENT_COUNT = 5



def get_nlp_loader(iterations=RELOAD_MODEL):
    '''Memoize and periodically reload the language model to clear the vocab and string store memory.
    Drastically increases runtime, but can save memory in case spaCy's own String Store gets to large.
    '''
    # The larger, but more accurate pre-trained french language model has to be installed with
    # `python -m spacy download fr_core_news_lg`
    nlp = spacy.load("fr_core_news_lg", exclude=['tagger', 'parser', 'lemmatizer', 'textcat'])
    nlp.max_length = 2_000_000
    tokenizer = nlp.tokenizer
    it = 1

    def loader():
        nonlocal it
        nonlocal nlp
        nonlocal tokenizer

        if iterations is not None and it % iterations == 0:
            logging.warning('reloading language model')
            nlp = spacy.load("fr_core_news_lg", exclude=['tagger', 'parser', 'lemmatizer', 'textcat'])
            nlp.max_length = 2_000_000
            tokenizer = nlp.tokenizer
        else:
            logging.info('reuse language model')

        it += 1
        return nlp, tokenizer
    
    return loader
        

   
def get_texts(pattern):
    '''Generator which yields all the file paths matching a given glob pattern.'''
    for path in glob(pattern):
        with open(path) as f:
            text = f.read()
        name = Path(path).name
        yield (name, text) 


def chunk_text(text, tokenizer, max_len=CHUNK_SIZE):
    '''Split a text up into chunks of a given word count.
    Returns a list of strings, even if only a single chunk is created.
    '''
    doc = tokenizer(text)
    if max_len is not None:
        yield from (doc[i:i+CHUNK_SIZE] for i in range(0, len(doc), CHUNK_SIZE))
    else:
        yield doc[:]


def get_ents_count(doc, variant='LOC'):
    '''Return most common named entities of given variant.'''
    return Counter([
        ent.text
        for ent in doc.ents
        if ent.label_ == variant
    ])


def sum_up_counters(counter_list):
    '''Given a list of `Counter`s, add all the counts up and
    return a comprehensive counter.
    '''
    return reduce(lambda a, b: a+b, counter_list)


def main():
    results = {}
    nlp_loader = get_nlp_loader()

    for name, text in get_texts(f'{PLAIN_TEXT_DIR}*.txt'):
        logging.warning(f'Working on text {name}')
        _, tokenizer = nlp_loader()

        # Keep track of the most frequent NEs of each chunk.
        loc_counters = []
        per_counters = []
        for chunk in chunk_text(text, tokenizer):
            logging.debug('got chunk')
            logging.debug(len(chunk))
            nlp, _ = nlp_loader()
            logging.debug(nlp)
            doc = nlp(chunk.text)            
            loc_counters.append(get_ents_count(doc))
            logging.debug('counted LOC')
            per_counters.append(get_ents_count(doc, 'PER'))
            logging.debug('counted PER')
        
        logging.info('have all subcounts')
        most_freq_loc = sum_up_counters(loc_counters)
        most_freq_per = sum_up_counters(per_counters)
        results[name] = (
            most_freq_loc.most_common(MOST_FREQUENT_COUNT),
            most_freq_per.most_common(MOST_FREQUENT_COUNT))
        
    # Organize data as pandas DataFrame and write to csv file.
    df = pd.DataFrame.from_dict(results, orient='index', columns=['LOC', 'PER'])
    df.to_csv(RESULT_FILE_PATH)


if __name__ == '__main__':
    main()
