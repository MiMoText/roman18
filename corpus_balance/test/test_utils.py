'''
Unit tests for the `utils.py` module.
'''

import unittest
from utils import parse_page_count
from utils import parse_distribution_format

class PageCountParseTest(unittest.TestCase):
    def test_single_page_count(self):
        self.assertEqual(123, parse_page_count('123')[0])

    def test_single_page_count_with_p(self):
        self.assertEqual(123, parse_page_count('123p.')[0])
    
    def test_simple_sequence(self):
        string = '123, 321 , 23p.'
        expected = [123, 321, 23]
        result = parse_page_count(string)
        self.assertListEqual(result, expected)
    
    def test_simple_roman_numeral(self):
        strings = 'xiv, xii, xl'
        expected = [14, 12, 40]
        results = parse_page_count(strings, count_preface=True)
        self.assertListEqual(results, expected)
    
    def test_combined_roman_numeral(self):
        string = 'ix + 123'
        expected = [9, 123]
        results = parse_page_count(string, count_preface=True)
        self.assertListEqual(results, expected)
    
    def test_simple_range(self):
        strings = [
            ' 100 - 120',
            '100-120',
            '100 -120 ',
            '100 –120',
            ' 100 – 120  ',
        ]
        for s in strings:
            result = parse_page_count(s)
            self.assertEqual(20, result[0])
    
    def test_combined_range(self):
        string = '123 , 235- 287, 288–300'
        expected = [123, 52, 12]
        results = parse_page_count(string)
        self.assertListEqual(expected, results)

    def test_simple_pour_entry(self):
        string = '123 (pour 128)'
        expected = 128
        results = parse_page_count(string)
        self.assertEqual(results[0], expected)
    
    def test_combined_pour_entry(self):
        string = 'xii + 288, 238(pour 256)p.'
        expected = [12, 288, 256]
        results = parse_page_count(string, count_preface=True)
        self.assertListEqual(results, expected)


class PageFormatParseTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertIsNone(parse_distribution_format(''))
    
    def test_invalid_size(self):
        with self.assertRaises(ValueError):
            parse_distribution_format('in-9000')
    
    def test_no_format_given(self):
        self.assertIsNone(parse_distribution_format('this is no format'))
    
    def test_with_hyphen(self):
        strings = ['in-8', 'in -8', 'in- 8', 'in - 8']
        for s in strings:
            self.assertEqual(parse_distribution_format(s), 'in-8')
    
    def test_with_n_dash(self):
        strings = ['in–4', 'in –4', 'in– 4', 'in – 4']
        for s in strings:
            self.assertEqual(parse_distribution_format(s), 'in-4')
    
    def test_with_m_dash(self):
        strings = ['in—12', 'in —12', 'in— 12', 'in — 12']
        for s in strings:
            self.assertEqual(parse_distribution_format(s), 'in-12')
    
    def test_with_prefix(self):
        string = 'bla in - 12'
        self.assertEqual(parse_distribution_format(string), 'in-12')

if __name__ == '__main__':
    unittest.main()