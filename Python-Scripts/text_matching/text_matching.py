# https://github.com/lit-mod-viz/middlemarch-critical-histories/blob/master/notebooks/anthologies-match.ipynb
# https://github.com/JonathanReeve/text-matcher/blob/master/examples/jupyter-example.ipynb
from os.path import join
import pandas as pd
import text_matcher
from text_matcher.matcher import Matcher, Text
import nltk
import glob
from os.path import basename
import os
import re
#import spacy
nltk.download("stopwords")


def read_file(txtfile, filename):
	# read file
	with open(txtfile, "r", encoding="utf-8") as infile:
		txt = infile.read()
	txt = re.sub("' ", "'", txt)	
	return txt

def find_matches(text_dict, search_text_name, search_text):
	
	# find matches with text_matcher
	# iterate over all texts and saves results in dictionary, i.e. number of matches, locations in both texts A and B
	matches_list = {}
	txt = Text(search_text, search_text_name)
	
	for i, val in text_dict.items():
		if i != search_text_name:
			matchtext = Text(val, i)
			numMatches, locA, locB = Matcher(txt, matchtext, threshold=15).match() 
			matches_list[i] = [numMatches, locA, locB]
			#print(type(matches_list), matches_list)
	return matches_list

def main():
	
	path = join("..", "..", "plain", "files", "*.txt")
	#path = join("..", "..", "plain", "matchingtestfiles", "*.txt")
	if not os.path.exists(join("..", "..", "text_matches_csv_files")):
		os.mkdir(join("..", "..", "text_matches_csv_files"))
		
	savepath = join("..", "..", "text_matches_csv_files")
	
	
	text_dict = {}
	#for infile in glob.glob(path):
	for infile in glob.glob(path):
		filename = basename(infile).split(".")[0]
		print(filename)
		# read file and add to dictionary: filenames as key, texts as value
		txt = read_file(infile, filename)
		text_dict[filename] = txt
	
	# iterate over complete text-dictionary
	for i, val in text_dict.items():
		
		# take key as index to compare it with all other texts
		search_text_name = i
		print(search_text_name)
		search_text = val
		# search for the matches, it returns a dictionary with all matches (also the 0 matches)
		matches = find_matches(text_dict, search_text_name, search_text)
		
		
		# create new dictionary to save all real matches and get the text-parts from Text A (i.e. key text) and Text B (i.e. one per one of all other texts)
		match_dict = {}
		for i1, val1 in matches.items():
			#print("i1, val1", i1, val1)
			if val1[0] > 0: # to get only texts where matches are found
				#print("vals", val1[0], val1[2])
				matches_in_search_text = val1[1]
				matches_in_matching_text = val1[2]
				#print(matches_in_search_text, matches_in_matching_text)
				# get textpart in A:
				for i, match in enumerate(matches_in_search_text):
					#print("match", i, match)
					#print("match text 1",val1[1])
					textA = search_text[match[0]-30:match[0]] + search_text[match[0]:match[1]].upper() + search_text[match[1]:match[1]+30]
					
					# get textpart in B:
					
					#print("match text 2", val1[2])
					b1 = matches_in_matching_text[i][0]
					#print("b1", b1)
					b2 = matches_in_matching_text[i][1]
					textB = text_dict[i1][b1-30:b1] + text_dict[i1][b1:b2].upper() + text_dict[i1][b2:b2+30]
					# add both text parts and the locations in dictionary
					match_dict["{}_{}".format(i1, i)] = [textA, textB, match, (b1, b2)]
					#print(val1[2][0])
		
		#print(match_dict)
		# create dataframe from dictionary and save it as csv --> for each text there will be a csv-document
		if match_dict:
			df_texts = pd.DataFrame(match_dict, index =["Text in {}".format(search_text_name), "Text in B", "Location in {}".format(search_text_name), "Location in B"]).T
			#print(df_texts)

			df_texts.to_csv(join(savepath, "thresh_15_{}_texts.csv".format(search_text_name)), encoding="utf8")
		
main()
