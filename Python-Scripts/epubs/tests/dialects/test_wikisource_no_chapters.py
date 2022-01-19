from unittest import TestCase

from dialects.wikisource_no_chapters import WikisourceNCEpubDialect 


class EpubWikisourceNCTest(TestCase):
    '''
    Test the modifications which are specific to sources from wikisource without chapters.
    '''

    def setUp(self):
        self.dialect = WikisourceNCEpubDialect()


    def test_split_titlepage(self):
        '''Ensure that the modified `split_titlepage()` works.'''
        text = '''
Stuff
## First
Text
## Second
More text
'''
        titlepage, rest = self.dialect.split_titlepage(text)
        self.assertEqual(titlepage, '\nStuff\n## First\nText\n')
        self.assertEqual(rest, '## Second\nMore text\n')


    def test_split_titlepage_from_start(self):
        '''split_titlepage() needs to deal with the marker being at the start of the doc.'''
        text = '''## First
Text
## Second
More text
'''
        titlepage, rest = self.dialect.split_titlepage(text)
        self.assertEqual(titlepage, '## First\nText\n')
        self.assertEqual(rest, '## Second\nMore text\n')