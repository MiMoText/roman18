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
    
    def test_split_titlepage(self):
        '''rousseauonline.ch sources need a custom titlepage split logic.'''
        text = '''## Jean-Jacques Rousseau  
Collection complète des oeuvres

#### 17 vol., in-4º, Genève, 1780-1789  
www.rousseauonline.ch

JEAN JACQUES ROUSSEAU

## LA REINE FANTASQUE,  CONTE

\[ca. 1754; Bibliothèque Publique de Neuchâtel ms. R. 37; 15 juin, 1758 Journal encyclopédique \(extraits\); Oeuvres de Jean Jaques Rousseau, Amsterdam, 1769; le Pléiade édition, t. II, pp. 1177-1192. == Du Peyrou/Moultou 1780-89 quarto Édition, t. VII, pp.199-220.\]

LA REINE FANTASQUE, *CONTE*.
'''
        titlepage, rest = self.dialect.split_titlepage(text)
        expected_tp = ''
        expected_rest = '\nLA REINE FANTASQUE, *CONTE*.\n'
        self.assertEqual(rest, expected_rest)