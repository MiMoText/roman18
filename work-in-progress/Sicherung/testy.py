from xml.etree.ElementTree import Element, SubElement, tostring, XML
from xml.etree import ElementTree
from xml.dom import minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
top = Element('top')

parent = SubElement(top, 'parent')

children = XML('''<root><child num="0" /><child num="1" /><child num="2" /></root> ''')
parent.extend(children)

print (prettify(top))

