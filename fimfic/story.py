from fimfic.const import *
from fimfic.ffobj import FimFicObj

import json

class Story(FimFicObj):

    def __init__(self, session, url, title=None, id=None, author_name=None, **kwargs):
        self.url = url
        self.title = title
        self.id = id
        self.author_name = author_name

#        'download_url_prefix': f"{URL_PREFIX}/story/download/{story_id}/",


    def download(self):
        # if not self.url:
        #   raise error
        pass


    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "id": self.id,
            'author_name': self.author_name
        }


    def to_json(self):
        return FimFicObj.to_json(self, self.to_dict())
