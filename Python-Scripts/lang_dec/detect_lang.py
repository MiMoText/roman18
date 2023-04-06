## script for automatically detect text passages that are not written in French
## using the spacy LanguageDetector by David Beauchemin, see https://pypi.org/project/spacy-language-detection/

from bs4 import BeautifulSoup
import spacy
from spacy import Language
from spacy_language_detection import LanguageDetector
from os.path import join
import glob
import os.path

# path to the xml-files
text_path = join("", "..", "..", "XML-TEI", "files", "*.xml")


def open_file(xml):
    # read xml file and extract the body of the file
    with open(xml, "r", encoding="utf8") as infile:
        xml = infile.read()
    soup = BeautifulSoup(xml, "xml")

    text_body = soup.body.text
    return text_body

def detect_lang(text, lang_dec_file):
    # detect languages

    def get_lang_detector(nlp, name):
        return LanguageDetector()

    nlp = spacy.load("fr_core_news_sm")
    Language.factory("language_detector", func=get_lang_detector)
    nlp.add_pipe("language_detector", last=True)
    
    doc = nlp(text)
    for i, sent in enumerate(doc.sents):
        lang = sent._.language
        if lang["language"] != "fr" and len(sent) >1:
            #print(sent, lang)
            lang_dec_file= lang_dec_file + str(sent) +  str(lang) +  "\n"
    
    return lang_dec_file



def main(text_path):
    
    for t in glob.glob(text_path):
        lang_dec_file = ""
        print(os.path.basename(t))
        filename = os.path.basename(t)
        filename_ext = filename.split(".")[0]

        if not os.path.isfile(join("lang_dec","lang-dec_file_{}.txt".format(filename_ext))):

            print(filename_ext)
            text = open_file(t)
            text = " ".join(text.split())

            lang_dec_file = lang_dec_file+ str(filename) + "\n"
            print(len(text))

            if len(str(text)) < 1000000:
                lang_dec_file = detect_lang(str(text), lang_dec_file)
                lang_dec_file = lang_dec_file + "\n ------------ \n"
            else:
                length = len(text)/2
                length = int(length)
                print(length)
                text1  = text[:length]
                text2 = text[length:]
                lang_dec_file1 = detect_lang(str(text1), lang_dec_file)
                lang_dec_file2 = detect_lang(str(text2), lang_dec_file)
                lang_dec_file = lang_dec_file + lang_dec_file1 + lang_dec_file2 + "\n ------------ \n"



            with open(join("to_do", "lang-dec_file_{}.txt".format(filename_ext)), "w", encoding="utf8") as outfile:
                outfile.write(lang_dec_file)

main(text_path)