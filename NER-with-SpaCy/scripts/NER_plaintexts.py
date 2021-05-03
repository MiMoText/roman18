import re
import nltk
import spacy
import spacy.cli
import glob
import csv

""" Medium model for better results """

nlp = spacy.load('fr_core_news_md', exclude=['tagger', 'parser', 'lemmatizer', 'textcat'])

""" List of all files in our folder """

file_list = glob.glob("../../plain/files/*.txt")
# print(file_list)

""" Max_length because the corpus is quite large """

nlp.max_length = 2000000

""" Dictionary including names of the plaintexts and the 5 most frequent LOC NE """

text_dict = {}
for file_path in file_list:
    print('Working on:', file_path.replace('../../plain/files/', ''))
    perm_file = open(file_path, 'r')
    perm_text = perm_file.read()
    perm_file.close()
    perm_doc = nlp(perm_text)
    most_freq_loc = nltk.FreqDist([(ent.text, ent.label_) for ent in perm_doc.ents if ent.label_ == 'LOC']).most_common(5)
    text_dict[file_path.replace('../../plain/files/', '')] = most_freq_loc


with open('ner_loc.csv', 'w', newline='') as file_output:
    tsv_output = csv.writer(file_output, delimiter='\t')
    tsv_output.writerow(text_dict.values())
    tsv_output.writerow(text_dict.keys())
