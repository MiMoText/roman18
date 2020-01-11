
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, XML
from xml.etree import ElementTree
from xml.dom import minidom

def prettify(elem):

    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

tree = ElementTree.parse('beispiel.xml')
root = tree.getroot()

parent = SubElement(root, 'body')




print(prettify(root))