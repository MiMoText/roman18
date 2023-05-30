# Script for combining the extisting modlist_final and the newly created modlist (see folders extend_modlist amd modlist_extension)


from os.path import join
import pandas as pd

path_new_modlist = join("modlist_extension", "modlist_extention_new_getrennt.csv")

path_modlist = join("", "extend_modlist" , "combined_modlist_and_wikisource_list.csv")

outpath = "modlist_final_v2.csv"


def read_modlists(path_new_modlist, path_modlist):

    with open(path_new_modlist, "r", encoding="utf8") as infile:
        new_modlist = pd.read_csv(infile, sep=",")
    
    new_modlist.drop(columns=["commentaire"], inplace=True)
    #print(new_modlist.head())

    with open(path_modlist, "r", encoding="utf8") as infile:
        old_modlist = pd.read_csv(infile, sep="=")
    #print(old_modlist.head())

    return new_modlist, old_modlist

def combine_modlists(new_modlist, old_modlist):

    new_modlist.rename(columns={"original": "hist", "modernisé":"modern"}, inplace=True)
    #print(len(new_modlist))
    #print(len(old_modlist))
    final_modlist = pd.concat([old_modlist, new_modlist], ignore_index=True)
    #print(len(final_modlist))
    print(final_modlist.head())

    return final_modlist

def save_new_modlist(outpath, final_modlist):

    with open(outpath, "w", encoding="utf8") as outfile:
        final_modlist.to_csv(outfile, sep="=", index=False, line_terminator="\n")

def main(path_new_modlist, path_modlist, outpath):

    new_modlist, old_modlist = read_modlists(path_new_modlist, path_modlist)
    final_modlist = combine_modlists(new_modlist, old_modlist)
    save_new_modlist(outpath, final_modlist)


main(path_new_modlist, path_modlist, outpath)


