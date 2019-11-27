
''' This Script generates Well-formed XML-Dokument from preprocessed with TUSTEP romans.'''

import re


def infile_read(file):
    """
    Takes as input a TXT file.
    Returns it as a string.
    """
    with open(file, "r", encoding="utf8") as infile:
        text = infile.read()
    return text

#path to the file, it takes one roman at once
clean = infile_read("D:/Downloads/roman-dixhuit/TEI-XML/Roman_bearbeitet/Beauharnais_Lettres.xml")

#setting the root-element, just to test whether it works, looking for better solution
clean = re.sub('<h><s n="E10"/></h>', '<TEI>\n<h><s n="E10"/></h>', clean)
clean = re.sub('<h><s n="E252"/></h>', '<h><s n="E252"/></h></TEI>', clean)

#delete filename-lines
clean = re.sub('<file name=".*?"/>', '', clean)
#clean = re.sub('<lb n=".*?"/', '<l', clean)

#delete these lines, because they bring no useful information
clean = re.sub('<pb n=.*?/>', '', clean)

#delete first 9 empty pages
clean = re.sub('<h><s n="E[1-9]"/></h>', '', clean)

#delete lines that have just --
clean = re.sub('<lb n=".*?"/>-+', '', clean)

#the <P/> for page break, destroys the XML-Order
clean = clean.replace('<P/>', '')
#clean = clean.replace('<Z>', '')
#clean = clean.replace('</Z>', '')
clean = clean.replace("^&", "&amp;")
clean = re.sub('<lb n=".*?"/><konghang.*?>', '', clean)

#'spr' destroys the XML-Order
clean = clean.replace('<spr>', '')
clean = clean.replace('</spr>', '')

#delete empy lines
clean = [line for line in clean.split('\n') if line.strip() != '']


#def adding(file):

   # lines = []
   # for line in file:
       # if line.startswith('<l>'):
        #    line += '</l>'
       # lines.append(line)
   # return lines


#cleaned = adding(clean)
cleaned = '\n'.join(clean)


#cleaned = cleaned.replace('</P></l>', '</l></P>')
#cleaned = cleaned.replace('<l><P>', '<P><l>')
#cleaned = re.sub('<P><l>\s+<Am1>', '<P><Am1><l>', cleaned)
#cleaned = cleaned.replace('</Am1></l></P>', '</l></Am1></P>')
#cleaned = cleaned.replace('<l><Am1>', '<Am1><l>')
#cleaned = cleaned.replace('</Am1></l>', '</l></Am1>')
#cleaned = cleaned.replace('<l><negEZ>', '<negEZ><l>')
#cleaned = cleaned.replace('</negEZ></l>', '</l></negEZ>')
print(cleaned)
f = open("changed.xml", 'w', encoding="utf8")
f.write(cleaned)
f.close








