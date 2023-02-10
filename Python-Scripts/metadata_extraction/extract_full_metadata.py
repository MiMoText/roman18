"""
Script for extracting Metadata of the MiMoText roman18 XML-TEI-files (https://github.com/MiMoText/roman18/tree/master/XML-TEI/files) based on the
Script https://github.com/COST-ELTeC/Scripts/blob/master/Python/extract_metadata.py

changed to fit the MiMoText structure and relevant metadata


#!/usr/bin/env python3
"""
# === Import statements ===

import os
import re
import glob
from os.path import join
from os.path import basename
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup as bs
from collections import Counter

# === Files and folders ===
path = "../../XML-TEI/files"

# === Parameters ===
xpaths = {"xmlid": "//tei:TEI/@xml:id",
          "title": "//tei:titleStmt/tei:title/text()",
          "author_wikidata": "//tei:titleStmt/tei:author/@ref",
          "printSource-yr": "//tei:bibl[@type='printSource']/tei:date/text()",
          "firsted-yr": "//tei:bibl[@type='firstEdition']/tei:date/text()",
          "form": "//tei:textClass/tei:keywords/tei:term[@type='form']/text()",
          "spelling": "//tei:textClass/tei:keywords/tei:term[@type='spelling']/text()",
          "data-capture": "//tei:textClass/tei:keywords/tei:term[@type='data-capture']/text()",
          "bgrf": "//tei:titleStmt/tei:title/@ref",
          "title_wikidata": "//tei:titleStmt/tei:title/@ref",
          "token_count": "//tei:extent/tei:measure/text()",
          "vols_count": "//tei:extent/tei:measure[@unit='vols']/text()",
          "lang": "/tei:TEI/@xml:lang",
          "publisher": "//tei:TEI//tei:publisher/@ref",
          "distributor": "//tei:TEI//tei:distributor/@ref",
          "distribution_date": "//tei:TEI//tei:publicationStmt/tei:date/text()",
          "copyright_status": "/tei:TEI//tei:licence/@target",
          "digitalSource_Title": "//tei:bibl[@type='digitalSource']/tei:title/text()",
          "digitalSource_Ref": "//tei:bibl[@type='digitalSource']/tei:ref[1]/@target",
          "digitalSource_Publisher": "//tei:bibl[@type='digitalSource']/tei:publisher[1]/text()",
          "digitalSource_Date": "//tei:bibl[@type='digitalSource']/tei:date/text()",
          "printSource_title": "//tei:bibl[@type='printSource']/tei:title/text()",
          "printSource_author": "//tei:bibl[@type='printSource']/tei:author/text()",
          "printSource_pubPlace": "//tei:bibl[@type='printSource']/tei:pubPlace/text()",
          "printSource_date": "//tei:bibl[@type='printSource']/tei:date/text()",
          "resp_datacapture": "//tei:respStmt[1]/tei:name/text()",
          "resp_encoding": "//tei:respStmt[2]/tei:name/text()",
          }

ordering = ["filename", "au-name", "au-birth", "au-death", "title", "au-gender", "firsted-yr", "printSource-yr", "form", "spelling",
            "data-capture", "token count", "vols_count", "size", "bgrf", "author_wikidata", "title_wikidata", "lang",
            "publisher", "distributor", "distribution_date", "copyright_status", "digitalSource_Title",
            "digitalSource_Ref",
            "digitalSource_Publisher", "digitalSource_Date", "printSource_title", "printSource_author",
            "printSource_pubPlace", "printSource_date", "resp_datacapture", "resp_encoding"]

sorting = ["filename", True]


# === Functions ===


def open_file(teiFile):
    """
	Open and parse the XML file. 
	Returns an XML tree.
	"""
    with open(teiFile, "r", encoding="utf8") as infile:
        xml = etree.parse(infile)

    with open(teiFile, "r", encoding="utf8") as infile:
        txt = infile.read()

    return xml, txt

def get_all_elements(metadatum):

    metas = ', '.join(str(word) for word in metadatum)
    #print(metas)

    return metas

def get_metadatum(xml, xpath, key):
    """
	For each metadata key and XPath defined above, retrieve the 
	metadata item from the XML tree.
	"""
    try:
        namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}
        metadatum = xml.xpath(xpath, namespaces=namespaces)#[0]
        #if len(metadatum) > 1:
        #    metadatum = get_all_elements(metadatum)
        #else:
        #    metadatum = metadatum[0]
        
    except:
        metadatum = "NA"




    if key == "title":
        metadatum = " ".join(metadatum[0].split())
        metadatum = re.sub(": MiMoText edition", "", metadatum)

    if key == "author_wikidata":
        #print("author wikidata ", metadatum)
        try:
            #metadatum = metadatum.split(" ")[1]
            #print("wiki", metadatum)
            #metadatum = re.sub("wikidata:", "", metadatum)
            
            metadatum = [w.split(" ")[1] for w in metadatum]
            metadatum = [re.sub("wikidata:", "", w) for w in metadatum]
            metadatum = ", ".join(m for m in metadatum)
            print(metadatum)
                
            if metadatum == "":
                metadatum = "NA"
        except IndexError:
            metadatum = "NA"

    if key == "bgrf":
        metadatum = [m.split(" ")[0] for m in metadatum]
        metadatum = [re.sub("bgrf:", "", m) for m in metadatum]
        metadatum = ", ".join(m for m in metadatum)

    if key == "title_wikidata":
        try:
            metadatum = [m.split(" ")[1] for m in metadatum]
            #print(metadatum)
            metadatum = [re.sub("wikidata:", "", m) for m in metadatum]
            metadatum = ", ".join(m for m in metadatum)
        except IndexError:
            metadatum = "NA"

    if key == "lang":
        try:
            metadatum = [m.split(" ")[0] for m in metadatum]
            metadatum = [re.sub("lang:", "", m) for m in metadatum]
            metadatum = ", ".join(m for m in metadatum)
        except IndexError:
            metadatum = "NA"

    if key == "publisher":
        try:
            metadatum = [m.split(" ")[0] for m in metadatum]
            metadatum = [re.sub("publisher:", "", m) for m in metadatum]
            metadatum = ", ".join(m for m in metadatum)
        except IndexError:
            metadatum = "NA"

    if key == "distributor":
        try:
            metadatum = [m.split(" ")[0] for m in metadatum]
            metadatum = [re.sub("distributor:", "", m) for m in metadatum]
            metadatum = ", ".join(m for m in metadatum)
        except IndexError:
            metadatum = "NA"

    if key == "distribution_date":
        try:
            metadatum = metadatum[0].split(" ")[1]
            metadatum = re.sub("distribution_date:", "", metadatum)
        except IndexError:
            metadatum = "NA"

    if key == "copyright_status":
        try:
            metadatum = metadatum[0].split(" ")[0]
            metadatum = re.sub("copyright_status:", "", metadatum)
        except IndexError:
            metadatum = "NA"

    if key == "digitalSource_Title":
        try:
            metadatum = re.sub("digitalSource_Title:", "", metadatum[0])
        except IndexError:
            metadatum = "NA"

    if key == "digitalSource_Ref":
        try:
            #metadatum = re.sub("digitalSource_Ref:", "", metadatum)
            metadatum = [re.sub("digitalSource_Ref:", "", w) for w in metadatum]
            metadatum = ", ".join(m for m in metadatum)
            print(metadatum)
        except IndexError:
            metadatum = "NA"

    if key == "digitalSource_Publisher":
        try:
            metadatum = [re.sub("digitalSource_Publisher:", "", m) for m in metadatum]
            metadatum = ", ".join(m for m in metadatum)
        except IndexError:
            metadatum = "NA"

    if key == "digitalSource_Date":
        try:
            metadatum = [re.sub("digitalSource_Date:", "", m) for m in metadatum]
            metadatum = ", ".join(m for m in metadatum)
        except IndexError:
            metadatum = "NA"

    if key == "printSource_title":
        try:
            metadatum = re.sub("printSource_title:", "", metadatum[0])
        except IndexError:
            metadatum = "NA"

    if key == "printSource_author":
        try:
            metadatum = [re.sub("printSource_author:", "", m) for m in metadatum]
            metadatum = ", ".join(m for m in metadatum)
        except IndexError:
            metadatum = "NA"

    if key == "printSource_pubPlace":
        try:
            metadatum = [re.sub("printSource_pubPlace:", "", m) for m in metadatum]
            metadatum = ", ".join(m for m in metadatum)
        except IndexError:
            metadatum = "NA"

    if key == "printSource_date":
        try:
            metadatum = [re.sub("printSource_date:", "", m) for m in metadatum]
            metadatum = ", ".join(m for m in metadatum)
        except IndexError:
            metadatum = "NA"

    if key == "resp_datacapture":
        try:
            metadatum = re.sub("resp_datacapture:", "", metadatum[0])
        except IndexError:
            metadatum = "NA"

    if key == "resp_encoding":
        try:
            metadatum = [re.sub("resp_encoding:", "", m) for m in metadatum]
            metadatum = ", ".join(m for m in metadatum)
        except IndexError:
            metadatum = "NA"

    if key == "firsted-yr" or key == "printSource-yr" or key == "form" or key == "spelling" or key == "data-capture" or key == "vols_count":
        try:
            metadatum = metadatum[0]
        except IndexError:
            metadatum = ""

    return metadatum


def get_authordata(xml):
    """
	Retrieve the author field and split it into constituent parts.
	Expected pattern: "name (alternatename) (birth-death)"
	where birth and death are both four-digit years. 
	The alternate name is ignored. 
	Note that the first and last names are not split into separate
	entries, as this is not always a trivial decision to make.
	Retrieve the author gender in second part.
	"""

    try:
        namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}
        authordata = xml.xpath("//tei:titleStmt/tei:author/text()",
                               namespaces=namespaces)

        authors_name_list = []
        birth_list = []
        death_list = []
        for entry in authordata:
            entry = " ".join(entry.split())
            if re.search("(.*?) \(", entry):
                name = re.search("(.*?) \(", entry).group(1)
                #print(name)
                authors_name_list.append(name)
                try:
                    birth = re.search("\((\d\d\d\d)", entry).group(1)
                    death = re.search("(\d\d\d\d)\)", entry).group(1)
                except:
                    birth = "NA"
                    death = "NA"
                birth_list.append(birth)
                death_list.append(death)
            elif re.search("(.*?)\(", entry):
                name = re.search("(.*?)\(", entry).group(1)
                authors_name_list.append(name)
                try:
                    birth = re.search("\((\d\d\d\d)", entry).group(1)
                    death = re.search("(\d\d\d\d)\)", entry).group(1)
                except:
                    birth = "xxxx"
                    death = "xxxx"
                birth_list.append(birth)
                death_list.append(death)
            else:
                name = entry
                authors_name_list.append(name)
                birth = "xxxx"
                birth_list.append(birth)
                death = "xxxx"
                death_list.append(death)
    except:
        name = "NA"
        birth = "NA"
        death = "NA"

    # get gender
    try:
        desc_nodes = xml.xpath("//tei:textDesc", namespaces=namespaces)
        n_list = []
        for n in desc_nodes:
            for t in n.findall(".//"):
                n_list.append(t.attrib["key"])
        au_gender = n_list[0]
        size = n_list[1]
    except:
        au_gender = "NA"

    names = ', '.join(str(word) for word in authors_name_list)
    births = ', '.join(str(word) for word in birth_list)
    deaths = ', '.join(str(word) for word in death_list)
    return names, births, deaths, au_gender, size


def get_count(txt):
    xml = bs(txt, "xml")
    body = xml.body.text
    count = re.findall("\W+", str(body))
    count = len(count)
    return count


def save_metadata(metadata, metadatafile, ordering, sorting):
    """
	Save all metadata to a CSV file. 
	The ordering of the columns follows the list defined above.
	"""
    metadata = pd.DataFrame(metadata)
    metadata = metadata.replace('\n', '', regex=True)
    metadata = metadata.applymap(lambda x: str(x).strip())
    metadata = metadata[ordering]
    metadata = metadata.sort_values(by=sorting[0], ascending=sorting[1])
    print(metadatafile)
    with open(join(metadatafile), "w", encoding="utf8") as outfile:
        metadata.to_csv(outfile, sep="\t", index=None, line_terminator="\n")


# === Coordinating function ===

def main(path, xpaths, ordering, sorting):
    # workingDir = join("..", "..", collection)

    teiFolder = join(path, "*.xml")
    metadatafile = join("..", "..", "XML-TEI", "xml-tei_full_metadata_test.tsv")
    allmetadata = []
    counter = 0
    for teiFile in glob.glob(teiFolder):
        filename, ext = basename(teiFile).split(".")
        print(filename)
        #try:
        if "schemas" not in filename:
            counter += 1
            keys = []
            metadata = []
            keys.append("filename")
            metadata.append(filename)
            xml, txt = open_file(teiFile)
            name, birth, death, au_gender, size = get_authordata(xml)
            count = get_count(txt)
            keys.extend(["au-name", "au-birth", "au-death", "au-gender", "token count", "size"])
            metadata.extend([name, birth, death, au_gender, count, size])
            for key, xpath in xpaths.items():
                metadatum = get_metadatum(xml, xpath, key)
                keys.append(key)
                metadata.append(metadatum)
                #print(metadata)
            allmetadata.append(dict(zip(keys, metadata)))
        #except:
        #    print("ERROR!!!", filename)
    print("FILES:", counter)
    save_metadata(allmetadata, metadatafile, ordering, sorting)


main(path, xpaths, ordering, sorting)
