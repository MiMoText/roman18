from enum import Enum

from .base import EpubBaseDialect
from .rousseau import RousseauEpubDialect
from .wikisource import WikisourceEpubDialect
from .wikisource_no_chapters import WikisourceNCEpubDialect


class EpubDialects(Enum):
    BASE = EpubBaseDialect
    ROUSSEAU = RousseauEpubDialect
    WIKISOURCE = WikisourceEpubDialect
    WIKISOURCE_NC = WikisourceNCEpubDialect
