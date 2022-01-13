import re

from .base import EpubBaseDialect


class RousseauEpubDialect(EpubBaseDialect):
    
    def clean_up(self, text):
        '''Delete and/or replace unnecessary text artifacts.
        
        Additionally to the regular clean up, remove page number markings
        which are specific to RousseauOnline sources.
        '''
        text = super().clean_up(text)

        # These files use '\[999\]' to indicate page numbers.
        text = re.sub(r'\\\[\d+\\\]', '', text)
        return text