# Script for downloading historical to modern French dictionary from https://fr.wikisource.org/wiki/Wikisource:Dictionnaire

## check if words are already in our modlist, 

import re
import requests
import pandas as pd
from os.path import join
from bs4 import BeautifulSoup as bs
from string import ascii_uppercase as auc


## Parameters

modlist_path = join("", "..", "modlist_final.csv")


def read_modlist(modlist_path):

    with open(modlist_path, "r", encoding="utf8") as infile:
        modlist = pd.read_csv(infile, sep="=", names =["hist", "modern"])
    
    #print(modlist)
    return modlist

def get_dictionary():
    list_all = []
    for char in auc:
        req =  requests.get(f"https://fr.wikisource.org/wiki/Wikisource:Dictionnaire/{char}")
        soup = bs(req.text, 'html.parser')
    
        soupfr = soup.find("div", {"id": "mw-content-text"})
        soupfr = soupfr.findAll("li")
        #fr_dict = [(item[0], item[1]) for item in (str(itemx).split(":") for itemx in soupfr)]
        #fr_dict = pd.DataFrame(columns=["hist", "modern"])
        list_all = list_all +  list(soupfr)
    return soupfr, list_all

def create_DataFrame(soupfr):
    soupfr2 = []
    for item in soupfr:
        item = str(item)
        item = re.sub("<li>", "", item)
        item = re.sub("</li>", "", item)
        item = re.sub(",", "", item)
        try:
            item1, item2 = str(item).split(":")
            soupfr2.append([item1.strip(), item2.strip()])
        except ValueError:
            print(item1, item2, item)
        #fr_dict["hist"] = item1
        #fr_dict["modern"] = item2
        

    fr_dict = pd.DataFrame(soupfr2, columns=["hist", "modern"])
    #print(fr_dict)

    return fr_dict

def combine_modslists(fr_dict, modlist):

    combined = pd.concat([fr_dict, modlist])
    print(len(combined))

    combined = combined.drop_duplicates(subset=["hist"])
    print(len(combined))


    return combined


def save_dataframe(fr_dict, savestring):

    with open(savestring, "w", encoding="utf8") as outfile:
        fr_dict.to_csv(outfile, sep="=", index=False, line_terminator="\n")

def main(modlist_path):
    modlist = read_modlist(modlist_path)
    fr_dict, list_all = get_dictionary()
    #print(list_all)
    fr_dict = create_DataFrame(list_all)
    #save_dataframe(fr_dict, "new_modlist_wikisource.csv")
    combined = combine_modslists(fr_dict, modlist)
    save_dataframe(combined, "combined_modlist_and_wikisource_list.csv")


main(modlist_path)



