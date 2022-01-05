'''
Various utility functions which are to be used in the context of the balance_analysis
notebook, but which are too intricate (and possibly even warrant their own unit tests)
to include them verbatim.
'''

import re


class MismatchingPageDataError(ValueError):
    '''This exception indicates that the `page_count_string` and
    `distribution_format_string` are mismatched in the sense that
    they suggest a different number of parts.
    '''

#
# RegExes for various types of page count literals
#
# Matches strings like '123 (pour 128)', which should yield 128.
POUR_PATTERN = re.compile('\d+\s*\(pour\s*(\d+)\s*\)')
# Matches strings like 'xiv', which should yield 14.
ROMAN_PATTERN = re.compile('m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})')
# Matches strings like '100 – 120', which should yield 20.
RANGE_PATTERN = re.compile('(\d+)\s?[-–]\s?(\d+)')
# Matches strings like '123p', which should yield 123.
SINGLE_PATTERN = re.compile('(\d+)p?')


def parse_roman(string):
    '''Parse roman numeral and return integer.'''
    numerals = {
        'm': 1000, 'cm': 900, 'd': 500, 'cd': 400, 'c': 100, 'xc': 90,
        'l': 50, 'xl': 40, 'x': 10, 'ix': 9, 'v': 5, 'iv': 4, 'i': 1,
    }
    if not ROMAN_PATTERN.match(string):
        raise ValueError(f'{string} is not a valid roman numeral')
    result = 0
    position = 0
    for roman, arabic in numerals.items():
        while string[position:position+len(roman)] == roman:
            result += arabic
            position += len(roman)
    return result


def parse_page_count(page_count_str, count_preface=False, expected_segments=None):
    '''Given a `page_count_string`, try to determine the number of pages.
    
    `count_preface`: whether to parse roman numerals, which indicate a preface
    `expected_segments`: integer, which indicates how many different page numbers
        are contained in `page_count_string`. If not None, differing results lead
        to an exception being thrown.
    
    Returns all page counts as list of integers.
    '''
    # Split on plus, comma and dot characters. Filter any empty segments,
    # strip surrounding whitespace.
    segments = [s.strip() for s in re.split('[+,.]', page_count_str) if s.strip()]

    if expected_segments is not None and len(segments) != expected_segments:
        msg = f'Got {len(segments)} page count segments, expected {expected_segments}.'
        raise MismatchingPageDataError(msg)
    
    def extract(s, count_preface=False):
        if POUR_PATTERN.match(s):
            return int(POUR_PATTERN.match(s).groups()[0])
        elif RANGE_PATTERN.match(s):
            m = RANGE_PATTERN.match(s)
            return int(m.groups()[1]) - int(m.groups()[0])
        elif SINGLE_PATTERN.match(s):
            return int(SINGLE_PATTERN.match(s).groups()[0])
        elif count_preface and ROMAN_PATTERN.match(s):
            return parse_roman(s)
 
    parsed = [extract(s, count_preface) for s in segments]
    # Filter out `None` results from e.g. ignored roman numerals.
    return [number for number in parsed if number]


def parse_distribution_format(dist_format_str):
    '''Given a `distribution_format_string`, try to determine format.
    
    Valid resulting formats are 'in-2', 'in-4', 'in-8', 'in-12', 'in-16', 'in-18', 'in-24', 'in-32'. 
    '''
    # Note: the delimiter can be a hyphen, an m-dash or an n-dash.
    valid = ['1', '2', '4', '8', '12', '16', '18', '24', '32']
    format_match = re.search('in\s*[-–—]\s*(\d+)', dist_format_str)
    if format_match:
        size = format_match.groups()[0]
        if size not in valid:
            raise ValueError(f'"in-{size}" is not a valid page format.')
        return f'in-{size}'
    elif dist_format_str == 'in-plano':
        return 'in-1'
    return None
