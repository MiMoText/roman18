from unittest import TestCase, skip

import lxml.etree as ET

from xml_utils import insert_markup


class InsertMarkupTextTest(TestCase):
    '''
    Test cases for the insertion of nodes based on the text of a node.
    '''
    def setUp(self):
        self.node = ET.Element('p')
        self.pattern = r'(\*not\*)'
        self.blueprint = ET.Element('hi')

    def test_insert_markup(self):
        '''Insert a single piece of markup in the middle of the node's text.'''
        self.node.text = 'to be or *not* to be'
        node = insert_markup(self.node, self.blueprint, self.pattern)
        expected = '<p>to be or <hi>not</hi> to be</p>'
        results = ET.tostring(node, encoding='unicode')
        self.assertEqual(results, expected)
    
    def test_insert_markup_at_start(self):
        '''Insert markup at the start of the node's text.'''
        self.node.text = '*not* to be sassy, but...'
        node = insert_markup(self.node, self.blueprint, self.pattern)
        expected = '<p><hi>not</hi> to be sassy, but...</p>'
        results = ET.tostring(node, encoding='unicode')
        self.assertEqual(results, expected)
    
    def test_insert_markup_at_end(self):
        '''Insert markup at the end of the node's text.'''
        self.node.text = 'do you think so? I do *not*'
        node = insert_markup(self.node, self.blueprint, self.pattern)
        expected = '<p>do you think so? I do <hi>not</hi></p>'
        results = ET.tostring(node, encoding='unicode')
        self.assertEqual(results, expected)
    
    def test_insert_more_markup(self):
        '''Insert multiple nodes in a node's text.'''
        self.node.text = 'to *not* be or *not* to be?'
        node = insert_markup(self.node, self.blueprint, self.pattern)
        expected = '<p>to <hi>not</hi> be or <hi>not</hi> to be?</p>'
        results = ET.tostring(node, encoding='unicode')
        self.assertEqual(results, expected)


class InsertMarkupTailTest(TestCase):
    '''
    Test cases for the insertion of nodes based on the tail of a node.
    '''
    
    def setUp(self):
        self.container = ET.Element('div')
        self.node = ET.SubElement(self.container, 'p')
        self.blueprint = ET.Element('hi')
        self.pattern = r'(\*not\*)'

    def test_insert_markup_tail(self):
        '''Insert markup in a node's tail.'''
        self.node.text = 'How '
        self.node.tail = 'to *not* be'
        node = insert_markup(self.container, self.blueprint, self.pattern)
        expected = '<div><p>How </p>to <hi>not</hi> be</div>'
        results = ET.tostring(node, encoding='unicode')
        self.assertEqual(results, expected)
    
    def test_insert_markup_start_tail(self):
        '''Insert markup at the start of a node's tail.'''
        self.node.text = 'How '
        self.node.tail = '*not* to be'
        node = insert_markup(self.container, self.blueprint, self.pattern)
        expected = '<div><p>How </p><hi>not</hi> to be</div>'
        results = ET.tostring(node, encoding='unicode')
        self.assertEqual(results, expected)
    
    def test_insert_more_markup_tail(self):
        '''Insert multiple nodes in a node's tail.'''
        self.node.text = 'How '
        self.node.tail = '*not* doing *not* what I wanted?'
        node = insert_markup(self.container, self.blueprint, self.pattern)
        expected = '<div><p>How </p><hi>not</hi> doing <hi>not</hi> what I wanted?</div>'
        results = ET.tostring(node, encoding='unicode')
        self.assertEqual(results, expected)
