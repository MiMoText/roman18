from .base import EpubBaseDialect


class WikisourceEpubDialect(EpubBaseDialect):
    '''Epub dialect for sources 
    
    Epubs from Wikisource have been the reference implementation,
    so for the moment we can re-use the base dialect without further
    modifications.
    '''