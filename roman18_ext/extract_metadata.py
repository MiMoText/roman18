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
from collections import Counter


# === Files and folders ===
path = "files"

# === Parameters === 
xpaths = {"xmlid" : "//tei:TEI/@xml:id", 
          "title" : "//tei:titleStmt/tei:title/text()",
          "wikidata" : "//tei:titleStmt/tei:author/@ref", 
          "printSource-yr" : "//tei:bibl[@type='printSource']/tei:date/text()",
          "firsted-yr" : "//tei:bibl[@type='firstEdition']/tei:date/text()",
          "form" : "//tei:textClass/tei:keywords/tei:term[@type='form']/text()"
          }

ordering = ["filename", "au-name", "title", "au-gender", "firsted-yr", "printSource-yr", "form"]

sorting = ["filename", True]


# === Functions ===


def open_file(teiFile): 
    """
    Open and parse the XML file. 
    Returns an XML tree.
    """
    with open(teiFile, "r", encoding="utf8") as infile:
        xml = etree.parse(infile)
        return xml



def get_metadatum(xml, xpath): 
    """
    For each metadata key and XPath defined above, retrieve the 
    metadata item from the XML tree.
    """
    try: 
        namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
        metadatum = xml.xpath(xpath, namespaces=namespaces)[0]
    except: 
        metadatum = "NA"
    metadatum = re.sub(": MiMoText edition", "", metadatum)
    """
    if re.search("wikidata", metadatum):
        viaf = (metadatum.split(";"))[0]
        metadatum = (metadatum.split(";")[1]).split(":")[1]
        if len(metadatum) == 0:
            metadatum = viaf
            
        #print(metadatum)
    """
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
        namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}       
        authordata = xml.xpath("//tei:titleStmt/tei:author/text()",
                               namespaces=namespaces)[0]       
        #print(authordata)
        if re.search("(.*?) \(", authordata):
            name = re.search("(.*?) \(", authordata).group(1)
            try:
                birth = re.search("\((\d\d\d\d)", authordata).group(1)
                death = re.search("(\d\d\d\d)\)", authordata).group(1)
            except:
                birth = "NA"
                death = "NA"
        elif re.search("(.*?)\(", authordata):
            name = re.search("(.*?)\(", authordata).group(1)
            try:
                birth = re.search("\((\d\d\d\d)", authordata).group(1)
                death = re.search("(\d\d\d\d)\)", authordata).group(1)
            except:
                birth = "NA"
                death = "NA"
        else:
            name = authordata
            birth = "NA"
            death = "NA"
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
                #
                #print("nodes ",t.attrib["key"])
                n_list.append(t.attrib["key"])
        au_gender = n_list[0]
    except:
        au_gender = "NA"
    #print(au_gender)
    return name,birth,death, au_gender



def save_metadata(metadata, metadatafile, ordering, sorting): 
    """
    Save all metadata to a CSV file. 
    The ordering of the columns follows the list defined above.
    """
    metadata = pd.DataFrame(metadata)
    metadata = metadata[ordering]
    metadata = metadata.sort_values(by=sorting[0], ascending=sorting[1])
    print(metadatafile)
    with open(join(metadatafile), "w", encoding="utf8") as outfile: 
        metadata.to_csv(outfile, sep="\t", index=None)


# === Coordinating function ===

def main(path, xpaths, ordering, sorting):
    #workingDir = join("..", "..", collection)
    
    teiFolder = join(path, "*.xml")
    metadatafile = join("xml-tei_metadata.tsv")
    allmetadata = []
    counter = 0
    for teiFile in glob.glob(teiFolder): 
        filename,ext = basename(teiFile).split(".")
        #print(filename)
        try: 
            if "schemas" not in filename:
                counter +=1
                keys = []
                metadata = []
                keys.append("filename")
                metadata.append(filename)
                xml = open_file(teiFile)
                name,birth,death, au_gender = get_authordata(xml)
                #print(au_gender)
                keys.extend(["au-name", "au-gender"])
                metadata.extend([name, au_gender])
                
                for key,xpath in xpaths.items():
                    #print(key, xpath)
                    metadatum = get_metadatum(xml, xpath)
                    keys.append(key)
                    metadata.append(metadatum)
                    #print(metadata)
                allmetadata.append(dict(zip(keys, metadata)))
        except: 
            print("ERROR!!!", filename)
    print("FILES:", counter)
    save_metadata(allmetadata, metadatafile, ordering, sorting)
    
main(path, xpaths, ordering, sorting)