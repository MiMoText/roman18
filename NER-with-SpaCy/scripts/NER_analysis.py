import re
import nltk
import spacy
import spacy.cli
import glob
import csv

spacy.cli.download('fr_core_news_sm')


nlp = spacy.load('fr_core_news_sm', exclude=['tagger', 'parser', 'lemmatizer', 'textcat'])


file_list = glob.glob("/Users/sarahreb/Desktop/JobDH/roman18/plain/files/*.txt")
nlp.max_length = 2000000

text_dict = {}
for file_path in file_list:
    print('Working on:', file_path)
    perm_file = open(file_path, 'r')
    perm_text = perm_file.read()
    perm_file.close()
    perm_doc = nlp(perm_text)
    most_freq_loc = nltk.FreqDist([(ent.text, ent.label_) for ent in perm_doc.ents if ent.label_ == 'LOC']).most_common(5)
    text_dict[file_path] = most_freq_loc


with open('/Users/sarahreb/Desktop/ner_loc.csv', 'w', newline='') as file_output:
    tsv_output = csv.writer(file_output, delimiter='\t')
    tsv_output.writerow(str(text_dict.values()).removeprefix('/Users/sarahreb/Desktop/JobDH/roman18/plain/files/'))
    tsv_output.writerow(text_dict.keys())



