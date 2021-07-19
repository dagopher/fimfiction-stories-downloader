import pprint

class FimFicObj:
    def __init__(self, *kwargs):
        pass

    def infodump(self):
        print(pprint.pformat(self.__dict__))


# vim: ts=4 sw=4 et tw=100 : 
