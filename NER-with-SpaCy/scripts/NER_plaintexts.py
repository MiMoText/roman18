import re
import nltk
import spacy
import spacy.cli
import glob
import csv
import pandas as pd

# spacy.cli.download('fr_core_news_sm')


nlp = spacy.load('fr_core_news_sm', exclude=['tagger', 'parser', 'lemmatizer', 'textcat'])


file_list = glob.glob("../../plain/files/*.txt")
nlp.max_length = 2000000

text_dict = {}
for file_path in file_list:
    print('Working on:', file_path)
    perm_file = open(file_path, 'r')
    perm_text = perm_file.read()
    perm_file.close()
    perm_doc = nlp(perm_text)
    most_freq_loc = nltk.FreqDist([(ent.text, ent.label_) for ent in perm_doc.ents if ent.label_ == 'LOC']).most_common(5)
    most_freq_per = nltk.FreqDist([(ent.text, ent.label_) for ent in perm_doc.ents if ent.label_ == 'PER']).most_common(5)
    text_dict[file_path.replace('/Users/sarahreb/Downloads/roman18/plain/files/', '')] = most_freq_loc, most_freq_per

""" Write data to .csv table"""
dataframe = pd.DataFrame.from_dict(text_dict, orient='index', columns=['LOC', 'PER']).to_csv('ner_loc.csv')




