"""
Script for extending the "names.txt"-file based on the character and location string from mimotextbase
 input is a json-file based on the results querying mimotextbase https://tinyurl.com/2p7ubtlr
"""
from os.path import join
import json
import re
# Path to json-file
json_path = join("", "names_locs_wikibase.json")

# Path to txt-files:
per_path = join("", "PER_and_LOC", "PER.txt")
loc_path = join("", "PER_and_LOC", "LOC.txt")

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
    names_locs = [re.sub("[=\(\)\[\]\:]", "", word) for word in names_locs]
    return names_locs


def main(json_path, per_path, loc_path):

    names_locs = read_json_file(json_path) # reading the json file
    txt_names_locs = read_txt_files(per_path, loc_path)
    names_locs.extend(txt_names_locs)
    names_locs = clean_list(names_locs) # clean the list of characters and locations
    print("len new list: ", len(names_locs))
    
    # read existing names file
    with open(join("..", "names.txt"), "r", encoding="utf8") as infile:
        old_names_file = infile.read().splitlines()
    print("len old list: ", len(old_names_file))

    # combine both the old and the new extracted names
    combined_list = old_names_file + names_locs
    print("len combined: ", len(combined_list))
    combined_list = sorted(set(combined_list)) # delete repetitions within the list
    print("len combined without repetitions: ", len(combined_list))
    # save the extended names list
    with open("names_ext.txt", "w", encoding="utf8") as outfile:
        for l in combined_list:
            outfile.write(f"{l.lower()}\n")


main(json_path, per_path, loc_path)
