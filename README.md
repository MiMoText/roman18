[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5040855.svg)](https://doi.org/10.5281/zenodo.5040855)

# roman18
Collection de romans français du dix-huitième siècle (1750-1800) / Collection of Eighteenth-Century French Novels (1750-1800)

## Introduction

This collection of Eighteenth-Century French Novels contains digital texts of novels created or first published between 1751 and 1800. The collection is created in the context of [Mining and Modeling Text](https://www.mimotext.uni-trier.de/en), a project which is located at the Trier Center for Digital Humanities ([TCDH](https://tcdh.uni-trier.de/en)) at Trier University. Work on the collection is ongoing.

## Corpus building

In the first step, about 40 novels have been carefully created by double keying. Using this first group of novels, an OCR-model has been trained in cooperation with Christian Reul (University of Würzburg), who is one of the developers of OCR4all. The result is an OCR model for French prints of the late 18th century. This model is available within OCR4all as [18th_century_french](https://github.com/Calamari-OCR/calamari_models).

Applying this OCR-model to additional scans provided by for instance Gallica (bnf.fr) and HathiTrust, a second group of novels which are not yet digitally available (or only in low quality) is now being produced.

A third group of texts, based on existing full texts (from Gallica, Google books or Wikisource) will hopefully help us reach about 200 volumes by the end of 2022.

At the beginning, corpus composition depended primarily on pragmatic criteria. We then proceeded and used additional metadata on the literary production to balance the corpus of full texts. A bibliography documenting the overall production of novels in the period is Angus Martin, Vivienne G. Mylne and Richard Frautschi, *Bibliographie du genre romanesque français 1751-1800*, 1977. We used this metadata to balance our corpus of texts regarding the parameters gender, year of first publication and narrative form. 

[![Balancing of the collection](https://raw.githubusercontent.com/MiMoText/balance_novels/main/img/corpus_vs_literary_production.png "First edition year in corpus and in overall literary production")

## Formats

The texts are provided in several different formats. For the texts from the first group, the original double keying files are available. In addition, a cleaned-up XML version closely reflecting the original documents’ layout is available (folder XML4OCR).

The master format for all texts is an XML format following the *Guidelines* of the Text Encoding Initiative (folder XML-TEI). The files are encoded in accordance with a relatively restrictive schema developed in the COST Action ‘Distant Reading for European Literary History’.

In addition, we provide plain text versions of the texts. However, these are best generated depending on individual needs using the scripts “tei2txt.py” & "tei2txt_run.py"(in the Scripts folder). 

## Structure of the repository
* Archiv: here we store files which were generated as intermediate.
* OCR4all_output: this folder is needed for our OCR4all digitization pipeline. The subfolders are used to organize a manual correction pipeline. 
* Python-Scripts: the scripts folder contains python scripts needed for corpus creation 
* Schemas: current versions of the ELTeC schema in RELAX NG are available from this repository
* XML-TEI: our corpus of french novels 1751-1800 in XML/TEI and metadata are stored here
* plain:  our corpus of french novels 1751-1800 in plain text is stored here
* roman18_ext: this folder contains further novels in XML/TEI which were sorted out and not included in the final MiMoText corpus

## Funding 
* Forschungsinitiative des Landes Rheinland-Pfalz 2019-2023

## Licence

All texts and scripts are in the public domain and can be reused without restrictions. We don’t claim any copyright or other rights on the transcription, markup or metadata. If you use our texts, for example in research or teaching, please reference this collection using the citation suggestion below.

## Citation suggestion

*Collection de romans français du dix-huitième siècle (1750-1800) / Eighteenth-Century French Novels (1750-1800)*, edited by Julia Röttgermann, with contributions from Julia Dudar, Anne Klee, Johanna Konstanciak, Amelie Probst, Sarah Rebecca Ondraszek and Christof Schöch. Release v0.2.0. Trier: TCDH, 2021. URL: https://github.com/mimotext/roman18. DOI: http://doi.org/10.5281/zenodo.5040855.
