import json

from fimfic.ffobj import FimFicObj

class Story(FimFicObj):

    def __init__(self, title=None, link=None, id=None, url=None, author_name=None, **kwargs):
        self.url = url
        self.title = title
        self.link = link
        self.id = id
        self.author_name = author_name

#        'download_url_prefix': f"{url_prefix}/story/download/{story_id}/",
#        'story_url': f"{url_prefix}{story_link}"


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
