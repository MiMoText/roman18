from unittest import TestCase

from dialects.rousseau import RousseauEpubDialect 


class EpubRousseauTest(TestCase):
    '''
    Test the modifications which are specific to sources from rousseauonline.ch.
    '''

    def setUp(self):
        self.dialect = RousseauEpubDialect()
    
    def test_cleanup_remove_pagenumbers(self):
        '''Additionally to the regular clean up, remove page number markings
        which are specific to RousseauOnline sources.
        '''
        text = '\[201\]'
        expected = ''
        results = self.dialect.clean_up(text)
        self.assertEqual(expected, results)
    
    def test_cleanup_with_context(self):
        '''Ensure that clean up still works in the middle of paragraphs.
        
        Note that the clean up does currently not remove superfluous whitespace, since
        this is irrelevant for the resulting XML.
        '''
        text = 'Enfin à force de dévotions si bien faites, à force de \[203\] médecines si sagement employées'
        expected = 'Enfin à force de dévotions si bien faites, à force de  médecines si sagement employées'
        results = self.dialect.clean_up(text)
        self.assertEqual(expected, results)