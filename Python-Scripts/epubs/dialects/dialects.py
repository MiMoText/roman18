from enum import Enum

from .rousseau import RousseauEpubDialect
from .wikisource import WikisourceEpubDialect


class EpubDialects(Enum):
    ROUSSEAU = RousseauEpubDialect
    WIKISOURCE = WikisourceEpubDialect
