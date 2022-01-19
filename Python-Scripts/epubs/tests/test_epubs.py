'''
Tests concerning the main `epubs.py` file. 
'''

from unittest import TestCase

from dialects.dialects import EpubDialects
from epubs import determine_dialect


class EpubDialectTest(TestCase):
    '''Epub dialect detection tests.'''


    def test_detect_rousseauonline(self):
        '''Ensure sources from rousseauonline.ch are detected correctly.'''
        text = '''
## Jean-Jacques Rousseau  
Collection complète des oeuvres

#### 17 vol., in-4º, Genève, 1780-1789  
www.rousseauonline.ch

JEAN JACQUES ROUSSEAU

## LA REINE FANTASQUE, CONTE

Il y avoit autrefois un Roi qui aimoit son peuple...
        '''
        expected = EpubDialects['ROUSSEAU'].value
        results = determine_dialect(text)
        self.assertIsInstance(results, expected)
    

    def test_detect_wikisource_with_chapters(self):
        '''Ensure sources from wikisource are detected correctly.'''
        text = '''
## Les Lettres d'Amabed

### Voltaire

##### Garnier, Paris, 1877

###### Exporté de Wikisource le 11 novembre 2021

LES LETTRES D'AMABED

### PREMIÈRE LETTRE  

D'AMABED À SHASTASID, GRAND BRAME DE MADURÉ.
'''
        expected = EpubDialects['WIKISOURCE'].value
        results = determine_dialect(text)
        self.assertIsInstance(results, expected)
    

    def test_detect_wikisource_without_chapters(self):
        '''Ensure sources from wikisource without chapters are detected correctly.'''
        text = '''
## La Petite Maison \(version de 1763\)

### Jean-François de Bastide

##### Librairie des Bibliophiles, Paris, 1879

###### Exporté de Wikisource le 11 janvier 2022

## **LA PETITE MAISON**

Cette maison unique est sur les bords de la Seine. Une avenue, conduisant à une patte d’oie,
'''
        expected = EpubDialects['WIKISOURCE_NC'].value
        results = determine_dialect(text)
        self.assertIsInstance(results, expected)
    
    
    def test_enforce_dialect(self):
        '''When enforcing usage of a dialect, make sure it is actually used.'''
        text = 'test'
        ds = (
            ('WIKISOURCE', EpubDialects['WIKISOURCE'].value),
            ('WIKISOURCE_NC', EpubDialects['WIKISOURCE_NC'].value),
            ('ROUSSEAU', EpubDialects['ROUSSEAU'].value),
        )
        for forced, expected in ds:
            results = determine_dialect(text, forced)
            self.assertIsInstance(results, expected)
