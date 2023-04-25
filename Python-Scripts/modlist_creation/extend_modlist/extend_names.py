"""
Script for extending the "names.txt"-file based on the character and location string from mimotextbase
 input is a json-file based on the results querying mimotextbase https://tinyurl.com/2p7ubtlr
"""
from os.path import join
import json
import re
import pandas as pd
from bs4 import BeautifulSoup as bs
import glob

# Path to json-file
json_path = join("", "names_locs_wikibase.json")

# Path to txt-files:
per_path = join("", "PER_and_LOC", "PER.txt")
loc_path = join("", "PER_and_LOC", "LOC.txt")

# Path to Frantext-Files:
frantext_path = join("", "proper_names_frantext.txt")

names_from_spellcheck = join("", "names_extracted_from_spellcheck.txt")

def read_json_file(json_path):
    # read the json file and extract character and location information
    with open(json_path, "r", encoding="utf8") as infile:
        names_locs_wikibase = json.load(infile)
    #print(names_locs_wikibase)
    names_locs = []
    for val in names_locs_wikibase:
        names_locs.append(val.get("characters"))
        names_locs.append(val.get("locations"))
    return names_locs

def read_txt_files(per_path, loc_path):

    paths = [per_path, loc_path]
    txt_names_locs = []
    for p in paths:
        with open(p, "r", encoding="utf8") as infile:
            lines = [line.rstrip() for line in infile]
        txt_names_locs.extend(lines)
    
    return txt_names_locs

def clean_list(names_locs):
    # As there are more items in a string, we need to extract those and clean up a little
    names_locs = [nl.split(",") for nl in names_locs if nl]
    names_locs = [item.strip() for nl in names_locs for item in nl]
    names_locs = [item.split(" ") for item in names_locs]
    names_locs = [item for nl in names_locs for item in nl]
    names_locs = [re.sub("[=\(\)\[\]\:\.]", "", word) for word in names_locs]
    return names_locs


def read_csv_file():
    
    
    path_to_file = join("", "PER_and_LOC", "sorted.csv")
    with open(path_to_file, "r", encoding="utf8") as infile:
        txt_names_locs_df = pd.read_csv(infile, sep=";")

    print(txt_names_locs_df.columns.to_list())

    per = txt_names_locs_df["PER"].dropna().tolist()
    loc = txt_names_locs_df["LOC"].dropna().tolist()
    #per_but_no_ne = txt_names_locs_df["PER but no NE"].dropna().tolist()
    #cat_loc_is_per_no_ne = txt_names_locs_df["Categorised LOC, is PER (no NE)"].dropna().tolist()
    cat_loc_is_per = txt_names_locs_df["Categorised LOC, is PER"].dropna().tolist()
    #cat_per_is_loc_no_ne = txt_names_locs_df["Categorised PER, is LOC (no NE)"].dropna().tolist()
    cat_per_is_loc = txt_names_locs_df["Categorised PER, is LOC"].dropna().tolist()
    #loc_no_ne = txt_names_locs_df["LOC but no NE"].dropna().tolist()

    txt_names_locs = per + loc +  cat_loc_is_per  + cat_per_is_loc  # + cat_loc_is_per_no_ne + cat_per_is_loc_no_ne + per_but_no_ne  + loc_no_ne


    return txt_names_locs

def add_article(wordslist):

    vowels = ["a", "e", "i", "o", "u", "é", "h",]
    wordslist_new = []

    for w in wordslist:
        if w[0] in vowels:
            add_d = "d'"+w
            add_l = "l'"+w
            wordslist_new.append(add_d)
            wordslist_new.append(add_l)
        elif re.search("’", w):
            new_apos = re.sub("’", "'" , w)
            wordslist_new.append(new_apos)
    
    
    print(len(wordslist), len(wordslist_new))
    combined = wordslist + wordslist_new
    print(len(combined))


    return combined

def read_textfile(frantextfile):

    #with open(frantextfile, "r", encoding="utf8") as infile:
    #    text = infile.read()
    #xmltext = bs(text, "xml")
    #print(xmltext)
    with open(frantextfile, "r", encoding="utf8") as infile:
        frantext = infile.read().splitlines()
    
    return frantext


def main(json_path, per_path, loc_path, frantext_path, names_from_spellcheck):
    # reading the json file
    names_locs = read_json_file(json_path) 
    
    #txt_names_locs = read_txt_files(per_path, loc_path)
    # read names csv file
    txt_names_locs = read_csv_file()
    
    # combined json and txt names
    names_locs.extend(txt_names_locs)
    # clean the list of characters and locations
    names_locs = clean_list(names_locs) 
    print("len new list: ", len(names_locs))
    #print(sorted(set(names_locs)))

    # read frantext files 
    frantext_names = read_textfile(frantext_path)
    names_spellcheck = read_textfile(names_from_spellcheck)


    # read existing names file
    with open(join("..", "names.txt"), "r", encoding="utf8") as infile:
        old_names_file = infile.read().splitlines()
    print("len old list: ", len(old_names_file))

    # combine both the old and the new extracted names
    combined_list = old_names_file + names_locs + frantext_names + names_spellcheck
    
    print("len combined: ", len(combined_list))
    combined_list = sorted(set(combined_list)) # delete repetitions within the list
    print("len combined without repetitions: ", len(combined_list))

    # remove whitespaces
    combined_list = [w for w in combined_list if w.strip()]
    
    # add Articles if Word starts with vowel:
    combined_list = add_article(combined_list)

    print("len combined with added articles", len(combined_list))

    # save the extended names list
    with open("names_ext_added_articles_added_frantext_names.txt", "w", encoding="utf8") as outfile:
        for l in combined_list:
            outfile.write(f"{l.lower()}\n")

main(json_path, per_path, loc_path, frantext_path, names_from_spellcheck)
