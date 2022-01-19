import re
from itertools import takewhile

from .base import EpubBaseDialect


class WikisourceNCEpubDialect(EpubBaseDialect):
    '''Epub dialect for sources without chapters from wikisource.

    This wikisource epub has no sub chapters, which means the
    indicator for the start of the main text section differs.
    Note that this should in theory also affect any chapter splitting
    logic, but since this behavior is currently limited to source files
    without any chapters anyway, we do not need to overwrite the
    `split_chapters()` method. 
    '''

    def split_titlepage(self, text):
        '''Split on the second occurence of "## ".'''
        # How to recognize the end of the titlepage
        marker = '(^|\n)## '
        # First occurrence
        _start, end = re.search(marker, text).span()
        # Note that these positions still need to be offset by the position of
        # the first match. We will also add one to the index so that the ending
        # newline belongs to the titlepage.
        end_of_titlepage, _end_of_match = re.search(marker, text[end:]).span()
        titlepage, rest = text[:end_of_titlepage+end+1], text[end_of_titlepage+end+1:]
        rest += '\n'

        return titlepage, rest