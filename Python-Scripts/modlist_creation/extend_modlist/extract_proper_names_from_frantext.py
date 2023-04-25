# Script for extracting proper names from frantext files

from os.path import join
from bs4 import BeautifulSoup as bs
import glob

# Path to Frantext-Files:
frantext_path = join("", "frantext", "*.xml") 

def read_frantext(frantextfile):

    with open(frantextfile, "r", encoding="utf8") as infile:
        text = infile.read()
    xmltext = bs(text, "xml")
    #print(xmltext)
    return xmltext


def extend_with_frantext(frantext_path):

    all_words = []
    for file in glob.glob(frantext_path):
        xml_file = read_frantext(file)
        words = []
        nps = xml_file.find_all(pos="NP")
        for np in nps:
            words.append(np["word"])
        words = list(set(words))
        all_words = all_words + words
    all_words = list(set(all_words))
    #print("set all words", len(all_words), "\n")
    return all_words

def main(frantext_path):

    franwords = extend_with_frantext(frantext_path)

    with open("proper_names_frantext.txt", "w", encoding="utf8") as outfile:
        for l in franwords:
            outfile.write(f"{l.lower()}\n")
main(frantext_path)