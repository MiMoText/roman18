# Script for adding header to sentiment files, add year, title and text
import glob
from os.path import join
import pandas as pd
import os.path

# Parameters
file_path = join("..", "..", "plain", "files", "*.txt")

# last part of savepath has to be adjusted to "mimotext" (instead of "testheader")
save_path = join("..", "..", "sentiments", "texts", "test_header")
metadatafile = join("..", "..", "XML-TEI", "xml-tei_metadata.tsv")

# Functions
def read_metadata(metadatafile):
	# read metadata file to get year and title
	
	with open(metadatafile, "r", encoding ="utf8") as infile:
		metadata = pd.read_csv(infile, sep="\t")
	
	print(metadata.head())
	return metadata

def read_file(txt):
	# read plain texts
	with open(txt, "r", encoding="utf8") as infile:
		text = infile.read()

	return text 
	
	
def add_metadata(metadata, text, name):
	# get title and year for each file from metadata-table
	
	try:
		# remove leading whitespace from text
		text = text.lstrip()
		
		# get year
		year = metadata.loc[metadata["filename"] == name, "firsted-yr"].values[0]
		#print(year)
		
		# get title
		title = metadata.loc[metadata["filename"] == name, "title"].values[0]
		
		# merge year title and text
		sentimenttext = "year={}\n".format(year) + "title={}\n".format(title) + "text=" + text
		#print(sentimenttext[:200])
	except IndexError:
		print("not found in metadatatable")
		sentimenttext = ""
		
	return sentimenttext
	
def save_text(sentimenttext, name, savepath):
	# write text to savepath
	
	with open(join(savepath, "{}.txt".format(name)), "w", encoding = "utf8") as outfile:
		outfile.write(sentimenttext)
	

def main(file_path,save_path, metadatafile):
	
	metadata = read_metadata(metadatafile)
	
	for txt in glob.glob(file_path):
		
		name = os.path.basename(txt).split(".")[0]
		print(name)
		
		text = read_file(txt)
		
		sentimenttext = add_metadata(metadata, text, name)
		if sentimenttext != "":
			save_sentimenttext = save_text(sentimenttext, name, save_path)


main(file_path,save_path, metadatafile)
