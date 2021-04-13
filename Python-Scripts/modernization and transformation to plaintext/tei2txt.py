"""
Script to extract plain text from XML-TEI. 
Run this using tei2txt_run.py 
"""

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


#==============
# Functions 
#==============



# === Getting ready

def helper(paths, params): 
	if not os.path.exists(paths["txtpath"]):
		os.makedirs(paths["txtpath"])


def get_filename(teifile): 
	filename, ext = os.path.basename(teifile).split(".")
	print(filename)
	return filename



# === Extracting the plain text

def read_tei(teifile): 
	with open(teifile, "r", encoding="utf8") as outfile: 
		tei = etree.parse(teifile)
		return tei


def remove_tags(tei, params): 
	namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
	etree.strip_tags(tei, "{http://www.tei-c.org/ns/1.0}hi")
	# other candidates: foreign, quote
	return tei


def remove_elements(tei, params): 
	namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
	for param in params.items(): 
		if params[param[0]] == False: 
			etree.strip_elements(tei, "{http://www.tei-c.org/ns/1.0}"+param[0], with_tail=False)
	return tei
	

def get_text(tei, params): 
	namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
	xpath = "//tei:text//text()"
	text = tei.xpath(xpath, namespaces=namespaces)
	text = " ".join(text)
	
	return text


def clean_text(text):

	text = re.sub("[ ]{2,20}", " ", text)
	text = re.sub("\n{2,20}", "\n", text)
	text = re.sub("[ \n]{2,20}", " \n", text)
	text = re.sub("\t{1,20}", "\t", text)
	list_text = list(text.split(" "))
	for i, word in enumerate(list_text[:-1]):
		if re.search("\n", list_text[i+1]):
			if not (re.search("\.", word) or  re.search("!", word) or  re.search("\?", word)):
				list_text[i+1] = re.sub("\n", " ", list_text[i+1])
			elif re.search("M\.", word):
				list_text[i+1] = re.sub("\n", " ", list_text[i+1])
				

	text = " ".join(list_text)
	text = re.sub("[ ]{2,20}", " ", text)
	text = re.sub(" \.", ".", text)
	text = re.sub(" ,", ",", text)
	text = re.sub(" ;",";", text)
	return text
	

def extract_text(tei, params):
	tei = remove_tags(tei, params)
	tei = remove_elements(tei, params)
	text = get_text(tei, params)
	text = clean_text(text)
	return text



# === Modernize the text

def get_mods(paths):
	with open(paths["modsfile"], "r", encoding="utf8", newline="\n") as infile: 
		mods = csv.reader(infile, delimiter="=")
		mods = {rows[0]:rows[1] for rows in mods}
		return mods


def modernize(text, mods): 
	for old,new in mods.items(): 
		old = "(\W)"+old+"(\W)"
		new = "\\1"+new+"\\2"
		text = re.sub(old, new, text)
	return text
	r'\bis\b'


def modernize_text(text, paths):
	mods = get_mods(paths)
	text = modernize(text, mods)
	return text


def correct_wordforms(text):
	'''
	Correction of vuid* -> vid*; phisio* -> physio*
	'''
	text = re.sub(r'(\s)(vuid)', r'\1vid', text) 
	text = re.sub(r'(\s)(phisio)', r'\1physio', text)
	return text

# === Normalize text ===

def normalize_text(text):
	text = re.sub("ſ", "s", text)
	text = re.sub("\.\ss", ". S", text)
	text = re.sub("\ns", "\nS", text)
	text = re.sub("\&", "et", text)
	return text

# === Save results to disk

def save_text(text, paths, filename): 
	filename = join(paths["txtpath"], filename+".txt")
	with open(filename, "w", encoding="utf8") as outfile: 
		outfile.write(text)
		
		

#==============
# Main 
#==============

def main(paths, params): 
	helper(paths, params)
	for teifile in glob.glob(paths["teipath"]):
		filename = get_filename(teifile)
		tei = read_tei(teifile)
		text = extract_text(tei, params)
		if params["modernize"] == True: 
			text = modernize_text(text, paths)
			text = correct_wordforms(text)
		else: 
			pass
		if params["normalize"] == True:
			text = normalize_text(text)
		#save_text(text, paths, filename)
	
	

