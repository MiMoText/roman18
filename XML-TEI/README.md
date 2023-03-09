# roman-dixhuit

Eighteenth-Century French Novels.

## Introduction

This repository of Eighteenth-Century French Novels contains digital texts of novels created or first published between 1751 and 1800. The collection is created in the context of Mining and Modeling Text, a project which is located at the Trier Center for Digital Humanities (TCDH) at Trier University. Work on the collection is ongoing until the end of 2023.

## Corpus building

In the first step, about 40 novels have been carefully created by double keying. Using this first group of novels, an OCR-model has been trained in cooperation with Christian Reul (University of Würzburg), who is one of the developers of OCR4all. The result is an OCR model for French prints of the late 18th century. This model is available within OCR4all. 

Applying this OCR-model to additional scans provided by for instance Gallica (bnf.fr), a second group of novels which are not yet digitally available (or only in low quality) is now being produced. 

A third group of texts, based on existing full texts (from Gallica, Google books or Wikisource) helped us reach about 200 novels by the end of 2022.

At the beginning, corpus composition depended primarily on pragmatic criteria. We then proceeded and used additional metadata on the literary production to balance the corpus of full texts. A bibliography documenting the overall production of novels in the period is Angus Martin, Vivienne G. Mylne and Richard Frautschi, Bibliographie du genre romanesque français 1751-1800, 1977. We used this metadata to balance our corpus of texts regarding the parameters gender, year of first publication and narrative form.

For a more detailed documentation of our sampling strategy, see our [Jupyter Notebook](https://github.com/MiMoText/balance_novels/blob/main/balance_analysis_newStructure.ipynb).

## Formats

The texts are provided in several different formats. For the texts from the first group, the original double keying files are available. In addition, a cleaned-up XML version closely reflecting the original documents’ layout is available (folder Archiv/XML4OCR). 

The master format for all texts is an XML format following the Guidelines of the Text Encoding Initiative (folder XML-TEI). The files are encoded in accordance with a relatively restrictive schema developed in the COST Action ‘Distant Reading for European Literary History’. 

In addition, we provide plain text versions of the texts. However, these are best generated depending on individual needs using the script “get_text.py” (in the Scripts folder). 

## Licence

All texts and scripts are in the public domain and can be reused without restrictions. We don’t claim any copyright or other rights on the transcription, markup or metadata. If you use our texts, for example in research or teaching, please reference this collection using the citation suggestion below. 

## Metadata 
The tsv-File xml-tei_full_metadata.tsv contains metadata on the XML/TEI-files. There is a short metadata version (xml-tei_metadata.tsv) and an extended metadata version (xml-tei_full_metadata.tsv).

* BGRF: The ID refers to Martin, Angus, Vivienne Mylne, and Richard L. Frautschi. Bibliographie du genre romanesque français, 1751-1800. London: Mansell, 1977. 
* VIAF: The ID referes to the Virtual International Authority File: https://viaf.org/
* Wikidata: The ID refers to the free and open knowledge base Wikidata: https://www.wikidata.org

## Citation suggestion

Collection de romans français du dix-huitième siècle (1751-1800) / Eighteenth-Century French Novels (1751-1800), edited by Julia Röttgermann, with contributions from Julia Dudar, Henning Gebhard, Anne Klee, Johanna Konstanciak, Damir Padieu, Amelie Probst, Sarah Rebecca Ondraszek and Christof Schöch. Release v0.3.0. Trier: TCDH, 2023. URL: https://github.com/mimotext/roman18. DOI: https://doi.org/10.5281/zenodo.7712928.
