# Work in progess: Topic Modeling pipeline for 18th century French novels

This repository contains scripts and test data used for the development of a topic modeling pipeline in the context of the project MiMoText.

The pipeline is based on the following set of scripts by Christof Schöch: https://github.com/dh-trier/topicmodeling/. It is constantly being revised and developed.

## Current implementations
* Splitting texts 
* Preprocessing: lemmatizing, POS-tagging, filtering by POS, stopword list and minimum word length

## How to

### Requirements

Please install the following: 

* Python 3
* Some additional libraries (with their respective dependencies): 
   * "pandas", see: https://pandas.pydata.org/
    * treetaggerwrapper, see: https://pypi.org/project/treetaggerwrapper/
* TreeTagger, see https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/
  * Please note: Follow the installation instructions given here; consider the differences between the different operating systems. It isn't necessary to download any language parameter files. They are already included in this folder.
    
 
### Application and usage notes

* Please make sure you have installed Python 3, TreeTagger and the desired libraries.
* Download and save the folder "topicmodeling". 
* Now you can run the scripts. 
* Run roman18_run.py. 
    * It calls all required scripts in the correct order.
    * You can change the following parameters:
       - **chunksize**: size of text parts (number of tokens) into which the novels are split
       - **lang**: language parameter to choose the model for POS-tagging; choose "fr" for modern French and "presto" for French of 16th/17th century.

* the splitted texts are saved in datasets/roman18-test/txt
* as the result of the preprocessing the texts are saved as lists of lemmas in results/rom18-test/pickles