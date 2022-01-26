import re

from .base import EpubBaseDialect


class RousseauEpubDialect(EpubBaseDialect):
    
    def clean_up(self, text):
        '''Delete and/or replace unnecessary text artifacts.
        
        Additionally to the regular clean up, remove page number markings
        which are specific to RousseauOnline sources.
        '''
        text = super().clean_up(text)

        # These files use markers like '\[999\]' to indicate page numbers.
        text = re.sub(r'\\\[\d+\\\]', '', text)
        return text
    
    def split_titlepage(self, text):
        '''Split document into titlepage and actual text.
        
        Source files from rousseauonline.ch have no consistent
        text formatting at the start of the actual text, but it
        seems to be the case that a metadata section is the last
        part of the titlepage, followed by a page number (which
        we already delete in `clean_up()`).
        The metadata section looks exactly like page number markers,
        except that it also includes non-numeric characters.
        '''
        # E.g. \[various characters, but at least one non-numeric\]
        pattern = r'\\\[(.*?\D+.*?)\\\]\n'
        titlepage, meta, rest = re.split(pattern, text)
        titlepage = f'{titlepage}\n{meta}\n'
        return titlepage, rest