from enum import Enum

from .base import EpubBaseDialect
from .rousseau import RousseauEpubDialect
from .wikisource import WikisourceEpubDialect


class EpubDialects(Enum):
    BASE = EpubBaseDialect
    ROUSSEAU = RousseauEpubDialect
    WIKISOURCE = WikisourceEpubDialect
