import os
from os.path import join
from bs4 import BeautifulSoup as bs
import glob
import re
import html
#############
# parameters
#############
path_to_xml_folder = join("..", "XML-TEI", "files", "*.xml")
outfile = join("..", "XML-TEI", "files_new")
stop_words = join("..", "work-in-progress", "Daten", "stopwords_full_version.txt")

def read_file(xml_file):
	with open(xml_file, "r", encoding="utf8") as infile:
		xml = infile.read()
	soup = bs(xml, "xml")
	return soup

def get_p_tags(xml, stopwords):
	
	body = xml.body
	
	for p in body.find_all(string= re.compile("p")):
		try:
			text = p
			text = re.sub("\n", " ", text)
			text = re.sub("- ", "-", text)
			text = re.sub(" -", "-", text)
			text = re.sub("<p>", " ", text)
			text = re.sub("</p>", " ", text)
			text = re.sub("<C>", "", text)
			text = re.sub("</C>", "", text)
			text = re.sub("<C/>", "", text)
			text = str(text).replace(str(text), " ".join(str(text).split()))
			text_split = list(text.split(" "))
			for ind, t in enumerate(text_split[:-1]):
				if t[-1] == "-" and t != "-":
					test_text = t + text_split[ind+1]
					test_text = re.sub("\.", "", test_text)
					test_text = re.sub(",", "", test_text)
					test_text = re.sub("\?", "", test_text)
					test_text = re.sub("!", "", test_text)
					test_text = re.sub(";", "", test_text)
					
					#print([test_text])
					try:
						test_text = test_text.split("'")[1]
		
					except IndexError:
						test_text = test_text
					
					if test_text not in stopwords:
					
						text = re.sub(t+text_split[ind+1],re.sub("-", "", t+text_split[ind+1]), text)
				#elif re.search("-", t) and not re.search("</hi>", t):
					#test_text = t
					#try:
						#test_text = test_text.split("'")[1]
		
					#except IndexError:
						#test_text = test_text
					
					#if test_text not in stopwords:
						#text = re.sub(t,re.sub("-", "", t), text)

			p.replace_with(text)
		except:
			continue
	return xml


def save_xml(xml, name, outfile):
	
	with open(join(outfile, "{}.xml".format(name)), "w", encoding="utf-8") as outfile:
		print("saving")
		outfile.write(xml.prettify())

def main(path_to_xml_folder, stop_words, outfile):

	with open (stop_words, "r", encoding="utf8") as infile:
		stopwords = infile.read()
	
	
	
	stopwords = list(stopwords.split(" "))
	for file in glob.glob(path_to_xml_folder):
		name = os.path.basename(file).split(".")[0]
		print(name)
		xml = read_file(file)
		xml = get_p_tags(xml, stopwords)
		save_xml(xml, name, outfile)

main(path_to_xml_folder, stop_words, outfile)
