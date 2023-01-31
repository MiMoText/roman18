As the corpus of the novels is now extended, the modlist used for the modernization is a bit outdated and will be extended.
This happens in various steps as follows:

1. First we are going to extend the names list for filtering proper names and location names using a json-File created from the output of querying the MiMoTextBase for characters and locations occuring in the novels: https://tinyurl.com/2p7ubtlr
By clicking on "Download" you can choose the "JSON file"-format.
This will be the input-file for the "extend_names.py"-Script.
Output: "names_ext.txt"

2. Creating new Spellcheck file:
Using the Script within the folder "spellcheck" we can create a new version of the spellcheck file as many novels were added to the corpus
Output: spellcheck_new.csv

4. Extract verbs to check them seperately as there is the option to replace historical to modern verbforms based on a script using the spellcheck-list created in step 2. Also using file "names_ext" to remove those words considered ok.
Also take the existing modlist to sort out those words that are already identified as historical french. Here the TreeTagger and TreeTaggerWrapper are used with the historical french language model "presto", which was already used for the TopicModeling process. For more information see https://github.com/MiMoText/topicmodeling

4. Append_modlist