from os.path import join
import treetaggerwrapper as ttw
from treetaggerwrapper import TreeTagger
import re
import pprint
import pandas as pd

#word_file_to_check = join("", "modlist_check_for_verbs.txt")
word_file_to_check = join("", "spellcheck_new.csv")
names_file = join("", "names_ext.txt")
existing_modlist = join("", "..", "modlist_final.csv")

def read_csv_file(csv_file):

    if csv_file == word_file_to_check:
        separator = ","
        names = None
    else:
        separator = "="
        names = ["old", "new"]

    with open(csv_file, "r", encoding="utf8") as infile:
        #words_to_check = infile.read().splitlines()
        csv_file_df = pd.read_csv(infile, delimiter=separator, names=names)

    return csv_file_df
    #words_to_check = words_to_check_file["Unnamed: 0"]
    #words_to_check_string = " ".join(str(val) for ind, val in words_to_check.items())

    #print(words_to_check_string)
    #words_to_check = set(words_to_check)
    #return words_to_check, words_to_check_string

def find_verbs(words_to_check, words_to_check_string, names, modlist_vals):
    # presto model for historical french
    # test_words = "J'y errois à-peu-près comme une plume legère, livrée au caprice du souffle qui l'agite; je ne sçavois si je montois ou si je descendois, ni ou j'allois, ni quand je cessois d'aller, & j'étois en proie à l'inquiétude la plus amère, lorsqu'après quelques heures d'une situation aussi cruelle, je reconnus une Région habitée, & vis devant moi un portail superbe, sur lequel étoit écrit en grandes lettres d'or,  Hôtel des Auteurs François."

    tagger = ttw.TreeTagger(TAGLANG='fr', TAGPARFILE="french_presto.par")
    #print("presto found")
    #words = tagger.tag_text(words_to_check)
    words = tagger.tag_text(words_to_check_string)
    print("words: ", words[:5])
    words = ttw.make_tags(words)
    print("len words ", len(words))
    poslist = ["Vvn", "Vvc", "Vun", "Vuc"]

    prepared = [item for item in words if item.word not in names]
    prepared = [item for item in prepared if item.word not in modlist_vals]
    #print("len words names sorted out", len(prepared), prepared[:5])
    prepared_verbs = [(item.word, item.lemma.lower()) for item in prepared if item.pos in poslist]
    print("prepared verbs: ", prepared_verbs[:5])
    print(len(prepared_verbs))

    prepared_others = [(item.word, item.lemma.lower()) for item in prepared if item.pos not in poslist]
    print("words not considered as verbs: ", len(prepared_others), prepared_others[:10])
    return prepared_verbs, prepared_others

def save_file(file, filename):
    with open("{}_from_spellcheck.csv".format(filename), "w", encoding="utf8") as outfile:
        file.to_csv(outfile, sep="=", index=False)


def main(word_file_to_check, names_file, existing_modlist):
    words_to_check = read_csv_file(word_file_to_check)
    modlist = read_csv_file(existing_modlist)
    #print(words_to_check.head())
    #print(modlist.columns.to_list())
    # some preparations:
    # use only first column in words_to_check and create one string of it
    words_to_check = words_to_check["Unnamed: 0"]
    words_to_check_string = " ".join(str(val) for ind, val in words_to_check.items())
    # get only column "old" from existing modlist
    modlist_vals = modlist["old"].to_list()
    #print(modlist_vals)

    with open(names_file, "r", encoding="utf8") as infile:
        namesfile = infile.read().splitlines()
    #print(namesfile)

    prepared_verbs, prepared_others = find_verbs(words_to_check, words_to_check_string, namesfile, modlist_vals)
    prepared_verbs_Series = pd.Series((word[0] for word in prepared_verbs))
    prepared_others_Series = pd.Series((word[0] for word in prepared_others))

    save_file(prepared_verbs_Series, "verbs")
    save_file(prepared_others_Series, "other_words")
    #with open("verbs_from_modlist.csv", "w", encoding="utf8") as outfile:
    #    prepared_verbs_Series.to_csv(outfile, sep="=")

main(word_file_to_check, names_file, existing_modlist)