import glob
import os.path
import pandas as pd
from os.path import join
from bs4 import BeautifulSoup
import re

filepath = join("", "..", "..", "XML-TEI" , "files", "*.xml")
metadata_path = join("", "xml-tei_full_metadata_update.tsv")
save_path = join("", "..", "..", "XML-TEI" , "files")

def read_table(metadata_path):

    with open(metadata_path, "r", encoding="utf8") as infile:
        metadata = pd.read_csv(infile, sep="\t", dtype=str, na_values="Nan", keep_default_na=False)
    return metadata

def read_xml(file):
    with open(file, "r", encoding="utf8") as infile:
        xml = BeautifulSoup(infile, "xml")
    return xml
    
def compare_title(filemetadata, xml_file):

    # find titleStmt
    titleStmt = xml_file.find("titleStmt")
    # find title:
    metatitle = filemetadata["title"]
    metatitle = metatitle.replace("\n", "")
    metatitle = " ".join(metatitle.split())
    metatitle = metatitle.split(": MiMoText")[0]

    xmltitle = titleStmt.title
    
    try:
        if xmltitle.string != metatitle:
            xmltitle.string = metatitle + ": MiMoText edition"
    except AttributeError:
        new_tag = xml_file.new_tag("title", ref="bgrf:0 wikidata:0")
        new_tag.string = filemetadata["title"] + ": MiMoText edition"
        xml_file.titleStmt.insert(1, new_tag)
    
    # find bgrf and wikidata
    xmlbgrf = xmltitle["ref"].split(" ")[0].split(":")[1]

    try:
        xmlwd = xmltitle["ref"].split(" ")[1].split(":")[1]
    except IndexError:
        
        xmltitle["ref"] = xmltitle["ref"] + " wikidata:0"
        print(xmltitle)
        xmlwd = xmltitle["ref"].split(" ")[1].split(":")[1]

    if xmlbgrf != filemetadata["bgrf"] or xmlwd != filemetadata["title_wikidata"]:
        xmltitle["ref"] = "bgrf:"+filemetadata["bgrf"] + " wikidata:"+ str(filemetadata["title_wikidata"])

    return xml_file

def compare_author(filemetadata, xml_file):

    # find author
    titleStmt = xml_file.find("titleStmt")
    xmlauthor = titleStmt.author

    if not re.search(",", filemetadata["au-name"]):
        xmlauthorref = xmlauthor["ref"].split(" ")
        print(xmlauthorref)
        try:
            xmlauthorwd = xmlauthorref[1].split(":")[1]
        except IndexError:
            xmlauthorref = xmlauthor["ref"].split(";")
            xmlauthor["ref"] = xmlauthor["ref"] + " wikidata:0"
            xmlauthorwd = xmlauthorref[1].split(":")[1]

        
        if xmlauthorwd != filemetadata["author_wikidata"]:
            xmlauthor["ref"] = xmlauthorref[0] + " wikidata:"+ str(filemetadata["author_wikidata"])


    if re.search(",", filemetadata["au-name"]):
        print(xmlauthor)
        meta_authors = filemetadata["au-name"].split(",")
        meta_births = filemetadata["au-birth"].split(",")
        meta_deaths = filemetadata["au-death"].split(",")
        meta_a_wd = filemetadata["author_wikidata"].split(",")
        authors = titleStmt.find_all("author")
        for ind, a in enumerate(authors):
            print (a.string, meta_authors[ind])
            try:
                birth = a.string.split("(")[1].split("-")[0]
                death = re.sub("\)", "", a.string.split("(")[1].split("-")[1])
                name = a.string.split("(")[0].strip()
                print("db found: ", birth, death, name)
            except IndexError:
                birth = "unknown"
                death = "unknown"
                name = a.string.strip()
                print("bd not found: ", birth, death, name)
            if name != meta_authors[ind] or birth != meta_births[ind] or death != meta_deaths[ind]:
                a.string = meta_authors[ind].strip() + "(" + meta_births[ind].strip() + "-" + meta_deaths[ind].strip() + ")"


        print(authors)

    return xml_file

def compare_respStmts(filemetadata, xml_file):

    # find respStmts
    titleStmt = xml_file.find("titleStmt")
    respStmts = titleStmt.find_all("respStmt")

    for res in respStmts:
        if res.resp.string.strip() == "data capture":
            if res.resp.next_sibling.next_sibling.string.strip() != filemetadata["resp_datacapture"]:
                res.resp.next_sibling.next_sibling.string = filemetadata["resp_datacapture"]
        
        elif res.resp.string.strip() == "encoding":
            if re.search(",", filemetadata["resp_encoding"]):
                all_resps_meta = filemetadata["resp_encoding"].split(",")
            else:
                all_resps_meta = [filemetadata["resp_encoding"]]

            all_resps = res.resp.find_next_siblings()

            for ind, respm in enumerate(all_resps_meta):
                try:
                    if all_resps[ind] != respm.strip():
                        all_resps[ind].string = respm.strip()
                except IndexError:
                    new_tag = xml_file.new_tag("name")
                    new_tag.string = respm.strip()
                    xml_file.respStmt.next_sibling.next_sibling.insert(ind+3, new_tag)
    return xml_file

def compare_extent(filemetadata, xml_file):

    # find extent
    extent = xml_file.find("extent")
    words = xml_file.find("measure", {"unit":"words"})
    if words.string != filemetadata["token count"]:
        words.string = filemetadata["token count"]
    vols = xml_file.find("measure", {"unit":"vols"})

    try:
        if vols.string != filemetadata["vols_count"]:
            vols.string = filemetadata["vols_count"]
    except AttributeError:
        new_tag = xml_file.new_tag("measure", unit="vols")
        new_tag.string = str(filemetadata["vols_count"])
        xml_file.extent.insert(2, new_tag)

    return xml_file

def compare_digSource(filemetadata, xml_file):

     # find sourceDesc: digital Source

    digitalSource = xml_file.find("bibl", {"type": "digitalSource"})
    metadSTitle = filemetadata["digitalSource_Title"]

    ## title
    try:
        if digitalSource.title.string != metadSTitle:
            digitalSource.title.string = metadSTitle
    except AttributeError:
        new_tag = xml_file.new_tag("title")
        new_tag.string = str(filemetadata["digitalSource_Title"])
        xml_file.bibl.insert(1, new_tag)


    counter = 2
    ## ref targets:
    if re.search(",", filemetadata['digitalSource_Ref']):
        meta_all_digrefs = filemetadata['digitalSource_Ref'].split(",")
    else:
        meta_all_digrefs = [filemetadata['digitalSource_Ref']]
    all_digrefs = digitalSource.find_all("ref")

    for ind, ref in enumerate(meta_all_digrefs):
        try:
            if all_digrefs[ind]["target"] != ref:
                all_digrefs[ind]["target"] = ref
            counter += 1
        except IndexError:
            new_tag = xml_file.new_tag("ref")
            new_tag["target"] = str(ref)
            xml_file.bibl.insert(counter, new_tag)
            counter += 1

    counterpubs = counter
    ## publisher
    if re.search(",", filemetadata['digitalSource_Publisher']):
        meta_all_digpubs = filemetadata['digitalSource_Publisher'].split(",")
    else:
        meta_all_digpubs = [filemetadata['digitalSource_Publisher']]

    all_digpubs = digitalSource.find_all("publisher")
    for ind, pub in enumerate(meta_all_digpubs):
        try:
            if all_digpubs[ind].string != pub:
                all_digpubs[ind].string = pub
            counterpubs += 1
        except IndexError:
            new_tag = xml_file.new_tag("publisher")
            new_tag.string = str(pub)
            xml_file.bibl.insert(counterpubs, new_tag)
            counterpubs += 1


    ## date
    if re.search(",", filemetadata['digitalSource_Date']):
        meta_all_digdates = filemetadata['digitalSource_Date'].split(",")
    else:
        meta_all_digdates = [filemetadata['digitalSource_Date']]

    #counter = 3
    all_digdates = digitalSource.find_all("date")
    for ind, date in enumerate(meta_all_digdates):
        try:
            if all_digdates[ind].string != str(date).strip():
                all_digdates[ind].string = str(date)
            
            xml_file.bibl.insert(counter+1, all_digdates[ind])
            counter += 2
        except IndexError:
            new_tag = xml_file.new_tag("date")
            new_tag.string = str(date)
            xml_file.bibl.insert(counter+1, new_tag)
            counter += 2



    return xml_file

def compare_printSource(filemetadata, xml_file):

    # sourceDesc: printSource:
    printSource = xml_file.find("bibl", {"type": "printSource"})
    
    ## title
    try:
        if printSource.title.string != filemetadata["printSource_title"]:
            printSource.title.string = str(filemetadata["printSource_title"])
    except AttributeError:
        new_tag = xml_file.new_tag("title")
        new_tag.string = str(filemetadata["printSource_title"])
        xml_file.bibl.insert(1, new_tag)

    
    if re.search(",", filemetadata['printSource_author']):
        meta_all_printauths = filemetadata['printSource_author'].split(",")
    else:
        meta_all_printauths = [filemetadata['printSource_author']]

    all_printauths = printSource.find_all("author")
    counter = 2
    for ind, pub in enumerate(meta_all_printauths):
        try:
            if all_printauths[ind].string != pub:
                print(all_printauths, pub)
                all_printauths[ind].string = pub
            printSource.insert(counter, all_printauths[ind])
            counter += 1
        except IndexError:
            new_tag = xml_file.new_tag("author")
            new_tag.string = str(pub)
            xml_file.bibl.insert(ind+counter, new_tag)
            counter += 1


    ## printSource date
    if printSource.date.string != filemetadata['printSource_date']:
        printSource.date.string = filemetadata['printSource_date']
    
    
    ## printSource pubplace
    if re.search(",", filemetadata['printSource_pubPlace']):
        meta_all_pubplaces = filemetadata['printSource_pubPlace'].split(",")
    else:
        meta_all_pubplaces = [filemetadata['printSource_pubPlace']]
    

    all_pubplaces = printSource.find_all("pubPlace")
    for ind, pub in enumerate(meta_all_pubplaces):
        try:
            if all_pubplaces[ind].string != pub:
                all_pubplaces[ind].string = pub
            printSource.insert(counter+1, all_pubplaces[ind])
            counter += 1
        except IndexError:
            new_tag = xml_file.new_tag("pubPlace")
            new_tag.string = str(pub)
            printSource.insert(counter+1, new_tag)
            counter += 1

    ## printSource publisher
    if re.search(",", filemetadata['printSource_publisher']):
        meta_all_publisher = filemetadata['printSource_publisher'].split(",")
    else:
        meta_all_publisher = [filemetadata['printSource_publisher']]
    

    all_publisher = printSource.find_all("publisher")
    for ind, pub in enumerate(meta_all_publisher):
        try:
            if all_publisher[ind].string != pub:
                all_publisher[ind].string = pub
            printSource.insert(counter+1, all_publisher[ind])
            counter += 1
        except IndexError:
            new_tag = xml_file.new_tag("publisher")
            new_tag.string = str(pub)
            printSource.insert(counter+1, new_tag)
            counter += 1



    ## first edition
    firsted = xml_file.find("bibl", {"type": "firstEdition"})
    try:
        if firsted.date.string != filemetadata["firsted-yr"]:
            firsted.date.string = filemetadata["firsted-yr"]
    except AttributeError:
        unspdate = xml_file.find("bibl", {"type":"unspecified"})
        if unspdate.date.string != filemetadata["firsted-yr"]:
            unspdate.date.string = filemetadata["firsted-yr"]

    

    return xml_file

def compare_profileDesc(filemetadata, xml_file):

    # find profileDesc
    xmlsize = xml_file.find("size")
    if xmlsize["key"] != filemetadata["size"]:
        xmlsize["key"] = filemetadata["size"]



    agender = xml_file.find("authorGender")
    if agender["key"] != filemetadata["au-gender"]:
        agender["key"] = filemetadata["au-gender"]
    
    form = xml_file.find("term", {"type": "form"})
    if form.string != filemetadata["form"]:
        form.string = filemetadata["form"]
    
    spelling = xml_file.find("term", {"type": "spelling"})
    if spelling.string != filemetadata["spelling"]:
        spelling.string = str(filemetadata["spelling"])

    datacap = xml_file.find("term", {"type": "data-capture"})
    if datacap.string != filemetadata["data-capture"]:
        datacap.string = str(filemetadata["data-capture"])

    

    return xml_file

def save_file(filename, xml_file, save_path):
    #save_file = etree.tostring(xml_file, encoding="utf8", pretty_print=True, xml_declaration=True)
    
    with open(join(save_path, filename), "w", encoding="utf8") as outfile:
        outfile.write(xml_file.prettify())

def main(metadata_path, filepath, save_path):
    metadata = read_table(metadata_path)
    #print(glob.glob(filepath))
    for file in glob.glob(filepath):
        filename = os.path.basename(file)
        
        for ind, row in metadata.iterrows():
            if os.path.basename(file).split('.')[0] == row["filename"]:# and re.search(",", row["resp_encoding"]):
                print(filename)
                #print("same", os.path.basename(file))
                xml_file = read_xml(file)
                filemetadata = row.to_dict()
                #xml_file = compare_title(filemetadata, xml_file)
                xml_file = compare_author(filemetadata, xml_file)
                #xml_file = compare_respStmts(filemetadata, xml_file)
                #xml_file = compare_extent(filemetadata, xml_file)
                #xml_file = compare_digSource(filemetadata, xml_file)
                #xml_file = compare_printSource(filemetadata, xml_file)
                #xml_file = compare_profileDesc(filemetadata, xml_file)
                save_file(filename, xml_file, save_path)
        print("\n\n")



main(metadata_path, filepath, save_path)