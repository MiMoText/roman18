"""
This file is used to adjust the settings and to run the 
extraction of plain text from XML-TEI files. 
"""

import tei2txt
from os.path import join


#=======================
# File paths
#=======================

wdir = ""
teipath = join(wdir, "..", "XML-TEI", "*.xml")
txtpath = join(wdir, "..", "plain", "files", "")
modsfile = join(wdir, "tei2txt_mods.csv")


#=======================
# Parameters
#=======================

head = True # Include chapter headings?
foreign = True # Include words marked as foreign?
note = False # Include text from footnotes?
pb = False # Include page breaks?
trailer = False # Include words marked as trailer?
quote = True # Include words marked as quote?
front = False # Include front matter?
back = False # Include back matter (other than notes)?

modernize = True # Modernize historical spelling?


# ======================
# Packaging 
# ======================

paths = {"teipath":teipath, "txtpath":txtpath, "modsfile":modsfile}
params = {"note":note, "head":head, "pb":pb, "foreign":foreign, "trailer":trailer, "front":front, "back":back, "quote":quote, "modernize":modernize}


#=======================
# Run tei2txt
#=======================

tei2txt.main(paths, params)
