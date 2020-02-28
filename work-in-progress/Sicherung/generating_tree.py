from xml.etree.ElementTree import Element, SubElement, Comment, tostring, XML
from xml.etree import ElementTree
from xml.dom import minidom


def prettify(elem):

    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

#parses the new-genereted XML-Document

#adding the information to TEI-Declaration
#root.set('xmlns', 'http://www.tei-c.org/ns/1.0')
top = Element('TEI')
#trying to generate the final TEI-tree
teiHeader = SubElement(top, 'teiHeader')
fileDesc = SubElement(teiHeader, 'fileDesc')
titleStmt = SubElement(fileDesc, 'titleStmt')
title = SubElement(titleStmt, 'title')
title.text = 'Lettres de Stephanie'
author = SubElement(titleStmt, 'author')
author.text = 'Fanny de Beauharnais'
publicationStmt = SubElement(fileDesc, 'publicationStmt')
sourceDesc = SubElement( fileDesc, 'sourceDesc')
text = SubElement(top, 'text')
front = SubElement(text, 'front')
div = SubElement (front, 'div')
body = SubElement(text, 'body', {'xml:lang':'fra'})

tree = ElementTree.parse('changed.xml')
root = tree.getroot()

#parent = SubElement(top, 'parent')

#children = XML('''<root><child num="0" /><child num="1" /><child num="2" /></root> ''')
#parent.extend(children)
print(prettify(root))
#tree.write('changed.xml')

