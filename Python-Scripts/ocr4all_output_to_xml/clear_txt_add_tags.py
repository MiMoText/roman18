# Script for cleaning ocr4all output from linebreaks and add minimal tags
# gedacht für die Bandergänzungen!

"""
Header - needs to be included
"""

header ="<hallo/>"
"""
header = <?xml-model href="../../Schemas/eltec-x.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<?xml-model href="../../Schemas/eltec-x.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>
<TEI xml:id="" xml:lang="fr" xmlns="http://www.tei-c.org/ns/1.0">
 <teiHeader>
  <fileDesc>
   <titleStmt>
    <title ref="bgrf:">MiMoText
     edition </title>
    <author ref="viaf:;wikidata:"></author>
    <respStmt>
     <resp> data capture</resp>
     <name></name>
    </respStmt>
   </titleStmt>
   <extent>
    <measure unit="words"></measure>
   </extent>
   <publicationStmt>
    <publisher ref="https://mimotext.uni-trier.de"> Mining and Modeling Text </publisher>
    <distributor ref="https://github.com/MiMoText/roman18"> Github </distributor>
    <date> 2021 </date>
    <availability>
     <licence target="https://creativecommons.org/publicdomain/zero/1.0/deed.en"/>
    </availability>
   </publicationStmt>
   <sourceDesc>
    <bibl type="digitalSource">
     <ref target=""/>
    </bibl>
    <bibl type="printSource">
     <date></date>
    </bibl>
    <bibl type="firstEdition">
     <date></date>
    </bibl>
   </sourceDesc>
  </fileDesc>
  <encodingDesc n="eltec-1">
   <p/>
  </encodingDesc>
  <profileDesc>
   <langUsage>
    <language ident="fra"/>
   </langUsage>
   <textClass>
    <keywords>
     <term type="form"></term>
     <term type="spelling"></term>
     <term type="data-capture">semi-automatic transcription</term>
    </keywords>
   </textClass>
   <textDesc>
    <authorGender key="" xmlns="http://distantreading.net/eltec/ns"/>
    <size key="" xmlns="http://distantreading.net/eltec/ns"/>
    <reprintCount key="unspecified" xmlns="http://distantreading.net/eltec/ns"/>
    <timeSlot key="T0" xmlns="http://distantreading.net/eltec/ns"/>
   </textDesc>
  </profileDesc>
  <revisionDesc>
   <change when=""> Initial ELTeC level-1 </change>
  </revisionDesc>
 </teiHeader>
 <text>
  <front>
  </front>
     <body>
"""

import glob
import os.path
from os.path import join
import os
import re
from bs4 import BeautifulSoup as bs
import itertools
# parameters

path = join("..", "..", "OCR4all_output", "txt", "corrected_and_to_be_sorted", "*.txt")

def read_file(file):
	# read file
	with open(file, "r", encoding="utf8") as infile:
		doc = infile.read()
		#print(doc)
	return doc

def clean_doc(doc, stopwords):
	# clear text from unnecessary linebreaks
	doc = doc.split(" ")
	#print(doc)
	doc_n = ""
	stop_words = ["il", "je,", "te", "vous", "nous", "elle", "elles", "ils", "toi", "moi", "on"]
	for ind, word in enumerate(doc):
		doc[ind] = re.sub("\n\n", "\n", word)

	for ind, word in enumerate(doc[:-1]):

		if re.search("-\n", word):
			word = re.sub("\n", "", word)
			word1 = word.split("-")[1]
			if word not in stop_words and word not in stopwords and word1 not in stop_words:
				word = re.sub("-", "", word)
				doc_n = doc_n + word + " "
			else:
				doc_n = doc_n + word + " "
		elif re.search("\n", word):
			word1 = word.split("\n")
			if re.search("\*", word1[0]):
				if not str(list(word1[1][0])).isupper():
					word = re.sub("\n", " ",word)
					doc_n = doc_n + word + " "
				else:
					doc_n = doc_n + word + " "
			elif re.search("[\.\?\!]", word1[0]):
				doc_n = doc_n + word + " "
			elif re.search("[\.\?\!]", word1[1]):
				word = re.sub("\n", " ", word)
				doc_n = doc_n + word + " "
			else:
				word = re.sub("\n", " ", word)
				doc_n = doc_n + word+ " "
		else:
			doc_n = doc_n + word + " "
	doc_n = doc_n + doc[-1]
	
	return doc_n
	

def schaft_s_sw(stopwords):
	# add schaft-s in stopwords for matching, not needed when text not historical
	stopwords_new = []
	for word in stopwords:
		wordl = list(word)
		wordlen = len(wordl)
		word_new = ""
		if wordlen > 1:
			for ind, w in enumerate(wordl[:-1]):
				if wordl[ind+1] != "-":
					w = re.sub("s", "ſ", w)
				word_new = word_new + w
			word_new = word_new + wordl[-1]
		stopwords_new.append(word)
		stopwords_new.append(word_new)
	return stopwords_new


def count_words(txt):
	# print count of text to terminal
	words = txt.split(" ")
	#print(words)
	count = len(words)
	print("Count", count)

	return count

def find_paragraphs(txt, header):
	# add tags: div and p
	doc = txt.split("\n")
	doc_new = "<div>"
	for p in doc:
		pall = "<p>" + p + "</p>"
		doc_new = doc_new + pall
	
	doc_new = doc_new + "</div></body></text></TEI>"
	
	doc_new = re.sub("&", "&amp;", doc_new)
	#print(doc_new)
	
	doc_new = header + doc_new
	soup = bs(doc_new, "xml")


	return soup

def find_divs(xml):
	# add head tag if chaputre or lettre found
	pall = xml.find_all("p")
	for p in pall:
		if re.search("CHAPITRE", p.text) or re.search("LETTRE", p.text):
			p.name = "head"
	allhead = xml.find_all("head")
	
	for h in allhead:
		ps = [i for i in itertools.takewhile(lambda x: x.name not in [h.name], h.next_siblings)]
		div = xml.new_tag("div")
		h.wrap(div)
		for tag in ps:
			div.append(tag)
	return xml
	
	
def save_xml(xml, name):
	# save xml
	if not os.path.exists("txt_to_xml"):
		os.mkdir("txt_to_xml")
	
	with open(join("txt_to_xml", "{}.xml".format(name)), "w", encoding="utf8") as outfile:
		outfile.write(str(xml))
		
		
def main(path, header):
	
	with open(join("..", "..", "work-in-progress", "Daten", "stopwords_full_version.txt"), "r", encoding="utf8") as infile:
		stopwords  = infile.read()
	
	
	with open(join("", "teiHeader-Template.xml"), "r", encoding="utf8") as infile:
		header = infile.read()

	stopwords = stopwords.split(" ")
	stopwords = schaft_s_sw(stopwords)
	
	for file in glob.glob(path):
		name = os.path.basename(file).split(".")[0]
		print(name)
		doc = read_file(file)
		doc = clean_doc(doc, stopwords)
		#count = count_words(doc)
		xml = find_paragraphs(doc, header)
		xml = find_divs(xml)
		print(xml)
		save_xml(xml, name)
main(path, header)
