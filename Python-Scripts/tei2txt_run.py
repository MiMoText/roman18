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
modpath = join(wdir, "modernization.csv")


#=======================
# Parameters
#=======================

heads = True # Include chapter headings?
foreign = True # Include words marked as foreign?
notes = False # Include text from footnotes?
pagebreaks = False # Include page breaks?
trailer = False # Include words marked as trailer?
quote = True # Include words marked as quote?
front = False # Include front matter?
back = False # Include back matter (other than notes)?

modernize = True # Modernize historical spelling?


# ======================
# Packaging 
# ======================

paths = {"teipath":teipath, "txtpath":txtpath, "modpath":modpath}
params = {"notes":notes, "modernize":modernize, "heads":heads, "pagebreaks":pagebreaks, "foreign":foreign, "trailer":trailer, "front":front, "back":back, "quote":quote}


#=======================
# Run tei2txt
#=======================

tei2txt.main(paths, params)
