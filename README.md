[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7712928.svg)](https://doi.org/10.5281/zenodo.7712928)

# Collection de romans français du dix-huitième siècle (1751-1800) / Collection of Eighteenth-Century French Novels (1751-1800)

This collection of Eighteenth-Century French Novels contains 200 digital texts of novels created or first published between 1751 and 1800. The collection is created in the context of [Mining and Modeling Text](https://www.mimotext.uni-trier.de/en) (2019-2023), a project which is located at the Trier Center for Digital Humanities ([TCDH](https://tcdh.uni-trier.de/en)) at Trier University. 

## Corpus building

In the first step, about 40 novels have been carefully created by double keying. Using this first group of novels, an OCR-model has been trained in cooperation with Christian Reul (University of Würzburg), who is one of the developers of OCR4all. The result is an OCR model for French prints of the late 18th century. This model is available within OCR4all as '18th_century_french'. As it was trained on OCR4all version 0.4.0, LAREX version 0.4.0, it is not compatible with the newest version of OCR4all. 

Applying this OCR-model to additional scans provided by for instance by Gallica (bnf.fr) and other sources (see metadata for details), a second group of novels which are not yet digitally available (or only in low quality) was produced.

A third group of texts, based on existing full texts (from Wikisource and other sources) helped us reach 200 volumes. 

## Balancing criteria
At the beginning, corpus composition depended primarily on pragmatic criteria. We then proceeded and used additional metadata on the literary production to balance the corpus of full texts. A bibliography documenting the overall production of novels in the period is Angus Martin, Vivienne G. Mylne and Richard Frautschi, *Bibliographie du genre romanesque français 1751-1800*, 1977. We used this metadata to balance our corpus of texts regarding the parameters gender, year of first publication and narrative form in approaching the historical distribution of these parameters in our full text metadata. 

### Year of first publication
The year of first publication according to BGRF data. We compared the overall novel publication with the corpus data and added novels per year according to the known historical publication proportions. 
![Balancing of the collection](https://raw.githubusercontent.com/MiMoText/balance_novels/main/img/pubyear-decade.png "First edition year in corpus and in overall literary production")

### Gender balance
Concerning gender, we used statements from Wikidata as well as a python script filtering for gender specific titles (Abbé, Marquis etc.). In cases where names lacked a Wikidata match or a specific title, we employed the gender guesser Python package to make gender predictions.
![Balancing of the collection](https://raw.githubusercontent.com/MiMoText/balance_novels/main/img/gender_proportion_without_unknown.png "Gender balance in corpus and in overall literary production")

### Narrative form 
Information on narrative form was extracted from the BGRF data (Mylne et al., 1977) supplemented by human evaluations conducted on the full texts.
![Balancing of the collection](https://raw.githubusercontent.com/MiMoText/balance_novels/main/img/narrative_forms_decade.png "Narrative form in corpus and in overall literary production")

For a more detailed documentation of our sampling and balancing strategy, see our [Jupyter Notebook](https://github.com/MiMoText/balance_novels/blob/main/balance_analysis_newStructure.ipynb).

## Formats: XML, plaintext (original or normalized)

The texts are provided in several different formats. For the texts from the first group, the original double keying files are available. In addition, a cleaned-up XML version closely reflecting the original documents’ layout is available (folder Archiv/XML4OCR).

The master format for all texts is an XML format following the *Guidelines* of the Text Encoding Initiative (folder XML-TEI). The files are encoded in accordance with a relatively restrictive schema developed in the [COST Action ‘Distant Reading for European Literary History’](https://www.distant-reading.net/) (level-1 encoding).
For pragmatic reasons, we have decided to deviate from this scheme in some cases and still generate valid documents. The following tags are affected:
- "timeSlot": As our corpus does not fit into the given ELTeC time-period, we use the metadatum "timeSlot" with key=T0.
- `<pb/>`: For digital source where page breaks were provided, we adopted those. For texts, which came from the OCR-pipeline, we omitted the pagebreaks.
- `<gap/>`: As for Table of contents or graphics we did not use the `<gap>`-Tag.
- `<milestone/>`: We did not use this tag for mid-chapter structural markings.
- Font change: We have marked non-French text passages with the tag `<foreign>`, in other places we have marked font changes, especially from digital sources where could re-use tags, with the tag `<hi>`.
As for the foreign text-passages we automatically detected the different languages, see https://github.com/MiMoText/roman18/tree/master/Python-Scripts/lang_dec and manually corrected the output before inserting the tags in the XML-files.

In addition, we provide plain text versions of the texts. However, these are best generated depending on individual needs using the scripts “tei2txt.py” & "tei2txt_run.py"(in the Scripts folder). 

The folder "plain" contains the files (within folder "files") with a basic normalization of historical spellings. The folder "files_non_modernized" contains the plaintext without normalization. Please note that some sources contain already modernized text from the beginning. All details on print and digital sources can be found in the teiHeader of the XML-files. 

## Metadata 
There is a short and an extensive metadata description in TSV for all TEI/XML files: 
* Metadata, short version: https://github.com/MiMoText/roman18/blob/master/XML-TEI/xml-tei_metadata.tsv
* Metadata, long version: https://github.com/MiMoText/roman18/blob/master/XML-TEI/xml-tei_full_metadata.tsv

| Column name | filename|  au-name   |title  |au-gender| firsted-yr| printSource-yr|
| ------------- | ------------- |------------- |------------- |------------- |------------- |------------- |
| Definition  | name of file|name of author |title of the novel | author [gender](https://distantreading.github.io/Schema/eltec-1.html#TEI.authorGender) |first year of publication |describes the year of the print source edition used as the source of the encoding which is not the first edition |


| Column name | form  |spelling  |data-capture| token count| size |
| ------------- | ------------- |------------- |------------- |------------- |------------- |
| Definition  | narrative form  |spelling (modern or historical) | mode of data capture |[token](https://distantreading.github.io/Schema/eltec-1.html#TEI.teidata.word) count |[size category](https://distantreading.github.io/Schema/eltec-1.html#TEI.size) following the scheme of ELTeC  |

|Column name  | bgrf|author_wikidata |title_wikidata |
| ------------- | ------------- |------------- |------------- |
|  Definition  | ID in *[Bibliographie du genre romanesque français](http://data.mimotext.uni-trier.de/wiki/Item:Q1)* (Martin / Mylne / Frautschi 1977) | Wikidata identifier of the author  | Wikidata identifier of the novel |

## Narrative forms

The controlled vocabulary of narrative forms consists of six possible values: homodiegetic, autodiegetic, heterodiegetic, epistolary, dialogue novel, mixed. 

![Narrative forms](https://raw.githubusercontent.com/MiMoText/ontology/main/module3_narrative-form/module3_narrative-form.png "Narrative forms")

## Language 

The main language of all texts is French. 

## Structure of the repository

* Archive: here we store files which were generated as intermediate for our digitization pipeline with OCR4all. 
* Python-Scripts: the scripts folder contains python scripts needed for corpus creation 
* Schemas: current versions of the ELTeC schema in RELAX NG are available from this repository
* XML-TEI: our corpus of french novels 1751-1800 in XML/TEI and metadata are stored here
* plain/files:  our corpus of french novels 1751-1800 in plain text is stored here
* plain/files_non_modernized: our corpus of french novels 1751-1800 is stored here in a normalized plain text version
* roman18_ext: this folder contains further novels in XML/TEI which were sorted out and not included in the final MiMoText corpus

## Licence

All texts and scripts are in the public domain and can be reused without restrictions. We don’t claim any copyright or other rights on the transcription, markup or metadata. If you use our texts, for example in research or teaching, please reference this collection using the citation suggestion below.

## Citation suggestion

*Collection de romans français du dix-huitième siècle (1751-1800) / Eighteenth-Century French Novels (1751-1800)*, edited by Julia Röttgermann, with contributions from Julia Dudar, Henning Gebhard, Anne Klee, Johanna Konstanciak, Damir Padieu, Amelie Probst, Sarah Rebecca Ondraszek and Christof Schöch. Release v 0.4.0. Trier: TCDH, 2023. URL: https://github.com/mimotext/roman18. DOI: https://doi.org/10.5281/zenodo.7712928.

## Related resources
* [
MiMoTextBase - a knowledge graph on Eighteenth Century French Novels](https://data.mimotext.uni-trier.de/wiki/Main_Page)
* [MiMoText SPARQL endpoint](https://query.mimotext.uni-trier.de/)
* [MiMoTextBase Tutorial: How to query the graph and an introduction to SPARQL](https://mimotext.github.io/MiMoTextBase_Tutorial/)
* [Our controlled vocabularies ](https://github.com/MiMoText/vocabularies)
* [MiMoText ontology ](https://github.com/MiMoText/ontology)

## Funding 

Forschungsinitiative des Landes Rheinland-Pfalz 2019-2023
