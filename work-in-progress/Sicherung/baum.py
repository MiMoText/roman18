from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom


def prettify(elem):

    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")



root = Element('TEI')
root.set('xmlns', 'http://www.tei-c.org/ns/1.0')

teiHeader = SubElement(root, 'teiHeader')
fileDesc = SubElement(teiHeader, 'fileDesc')
titleStmt = SubElement(fileDesc, 'titleStmt')
title = SubElement(titleStmt, 'title')
title.text = 'Lettres de Stephanie'
author = SubElement(titleStmt, 'author')
author.text = 'Fanny de Beauharnais'
publicationStmt = SubElement(fileDesc, 'publicationStmt')
sourceDesc = SubElement( fileDesc, 'sourceDesc')
text = SubElement(root, 'text')
front = SubElement(text, 'front')
div = SubElement (front, 'div')
body = SubElement(text, 'body', {'xml:lang':'fra'})

tree = ElementTree.parse('changed.xml')
roman = tree.getroot()




print(prettify(root))


