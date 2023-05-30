As the corpus of the novels is now extended, the modlist used for the modernization is a bit outdated and will be extended.
This happens in various steps as follows:

1. Extracting proper names from various sources - see folder "extend_names_list":

1.1 MiMoTextBase - Character names and narrative locations

First we are going to extend the names list for filtering proper names and location names using a json-File created from the output of querying the MiMoTextBase for characters and locations occuring in the novels: https://tinyurl.com/2p7ubtlr
By clicking on "Download" you can choose the "JSON file"-format.
This will be the input-file for the "extend_names.py"-Script.


1.2 NER in the novels

Also the txt-Files "LOC.txt" and "PER.txt" within the folder "PER_and_LOC" is used to extend the list. These lists were created by using the Script  github.com/MiMoText/NER_novels/blob/main/scripts/NER_novels.py using the MOST_FREQUENT_COUNT=10. The output of that script was then manually sorted in proper names and locations as it contained more than those.

1.4 POS-Tagging Frantext

As we use Frantext (https://www.frantext.fr/) as one of our sources for the corpus, we could re-use the POS-Tagging of those texts. In the script "extract_proper_names_from_frantext.py" those words tagged with a "NP" were extracted and saved as "proper_names_frantext.txt"

1.5 Proper names from the ongoing process

During the process of creating and modernizing a new modlist by a french speaking student assisstent, he sorted out the proper names that were falsely categorised as spelling errors. Those are found in the folder "modlist_extension".

Output: "names_ext_v2.txt"

2. Creating new Spellcheck file:
Using the Script within the folder "spellcheck" we can create a new version of the spellcheck file as many novels were added to the corpus
Output: spellcheck_new.csv

3. Get historical to modern Dictionary from Wikisource:
In the script "get_hist_french_dict.py" the dictionary found here https://fr.wikisource.org/wiki/Wikisource:Dictionnaire
 is downloaded and saved as "combined_modlist_and_wikisource_list.csv"

4. Using file "names_ext_v2" to remove those words considered ok.
Also take the existing modlist to sort out those words that are already identified as historical french. Here the TreeTagger and TreeTaggerWrapper are used with the historical french language model "presto", which was already used for the TopicModeling process. For more information see https://github.com/MiMoText/topicmodeling

4. Append_modlist