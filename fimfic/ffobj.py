import json
import pprint

class FimFicObj:
    def __init__(self, **kwargs):
        pass


    def infodump(self):
        print(pprint.pformat(self.__dict__))


    def to_json(self, data, **kwargs):
        return json.dumps(data)

# vim: ts=4 sw=4 et tw=100 : 
