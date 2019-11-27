'''This Script works only with well-formed XML-Document and modifies/changes this, still in the progress'''

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom


def prettify(elem):

    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

#parses the new-genereted XML-Document
tree = ElementTree.parse('changed.xml')
root = tree.getroot()

#adding the information to TEI-Declaration
root.set('xmlns', 'http://www.tei-c.org/ns/1.0')

#trying to generate the final TEI-tree
#teiHeader = SubElement(root, 'teiHeader')
#fileDesc = SubElement(teiHeader, 'fileDesc')
#titleStmt = SubElement(fileDesc, 'titleStmt')
#title = SubElement(titleStmt, 'title')
#title.text = 'Lettres de Stephanie'
#author = SubElement(titleStmt, 'author')
#author.text = 'Fanny de Beauharnais'
#publicationStmt = SubElement(fileDesc, 'publicationStmt')
#sourceDesc = SubElement( fileDesc, 'sourceDesc')
#text = SubElement(root, 'text')
#front = SubElement(text, 'front')
#div = SubElement (front, 'div')
#body = SubElement(text, 'body', {'xml:lang':'fra'})

print(prettify(root))