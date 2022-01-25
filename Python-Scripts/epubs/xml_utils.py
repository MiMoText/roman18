'''
Common functionality for handling XML.
'''

import re

import lxml.etree as ET
from lxml.etree import Element


def _create_ref(tbc, segment):
    number = ''.join(c for c in segment if c.isnumeric())
    number = f'#N{number}'
    elem = Element(tbc.tag, attrib={'target': number})
    return elem

def _create_hi(tbc, segment):
    content = segment.strip('*')
    elem = Element(tbc.tag, attrib=tbc.attrib)
    elem.text = content
    return elem

def _create_head(tbc, segment):
    content = segment.strip('# \n')
    elem = Element(tbc.tag, attrib=tbc.attrib)
    elem.text = content
    return elem

def _create_p(tbc, segment):
    content = segment.strip()
    elem = Element(tbc.tag)
    elem.text = content
    return elem

def insert_markup(node, tbc, pattern):
    '''Process an XML node, creating child nodes for certain markup.
    
    :param Element node: node to process
    :param Element tbc: node which serves as blueprint of what is "to be created"
    :param str pattern: regex pattern which detects segments which should be marked up
    :return the modified node
    :rtype Element 
    '''
    texts = re.split(pattern, node.text or '')
    tails = re.split(pattern, node.tail or '')

    texts = [t for t in texts if t]
    tails = [t for t in tails if t]

    # The latest node that we have created.
    last = node
    for i, segment in enumerate(texts):
        # If the segment matches our split pattern it means that we need
        # to create a new node.
        if re.match(pattern, segment):
            if tbc.tag=='hi':
                new = _create_hi(tbc, segment)
            elif tbc.tag=='ref':
                new = _create_ref(tbc, segment)
            elif tbc.tag=='head':
                new = _create_head(tbc, segment)
            elif tbc.tag=='p':
                new = _create_p(tbc, segment)
            else:
                raise ValueError(f'{tbc.tag} must be "hi", "ref", "head" or "p".')
            # If we haven't created a new node before, it is crucial that
            # we insert the new node as the very first child node, ignoring
            # any children that might have been present before.
            if last == node:
                node.insert(0, new)
            # If we have created a new node before, insert the new node
            # directly after it.
            else:
                insert_after(new, last)
            # Remember the latest node that we have created.
            last = new
            # If our match happened at the very beginning of the node's text, that
            # means that the node's text should now be empty, since its content is
            # now part of the newly created node.
            if i == 0:
                node.text = None
        # If there is no match and we are still at the very beginning of the
        # initial node then the current segment should remain in its text part.
        elif i == 0:
            node.text = segment
        # In every other case the non-matching text should be stored in the
        # tail of whichever node we have created last.
        else:
            last.tail = segment

    last = node
    for i, segment in enumerate(tails):
        if re.match(pattern, segment):
            if tbc.tag=='hi':
                new = _create_hi(tbc, segment)
            elif tbc.tag=='ref':
                new = _create_ref(tbc, segment)
            elif tbc.tag=='head':
                new = _create_head(tbc, segment)
            elif tbc.tag=='p':
                new = _create_p(tbc, segment)
            else:
                raise ValueError(f'{tbc.tag} must be "hi", "ref", "head" or "p".')
            new = insert_after(new, last)
            last = new
            # If our match happened at the very beginning of the tail, we need to erase the
            # original tail, because its whole content will end up in newly created nodes.
            if i == 0:
                node.tail = None
        elif i == 0:
            # If there is no match and we are still at the very beginning of the
            # original tail, then this current segment should remain as the sole tail.
            node.tail = segment
        else:
            last.tail = segment

    # Do the same for all child nodes of the current node.
    for child in node.getchildren():
        insert_markup(child, tbc, pattern)

    return node

        
def insert_after(node, previous):
    '''Insert `node` as a sibling of and directly following `previous` node.'''
    parent = previous.getparent()
    parent.insert(parent.index(previous)+1, node)
    return node
