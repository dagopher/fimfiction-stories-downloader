from .bookshelf import Bookshelf
from .ffobj import FimFicObj
from .session import Session
from .story import Story

__all__ = [
    "Bookshelf",
    "Session",
    "Story",
]

class FimficObj:
    def __init__(self, *kwargs):
        pass

    def infodump(self):
        print(pprint.pformat(self.__dict__))

# vim: ts=4 sw=4 et tw=100 : 
