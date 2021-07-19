from fimfic.ffobj import FimFicObj

class Story(FimFicObj):
    def __init__(self, title=None, link=None, id=None, url=None, author_name=None, **kwargs):
        self.url = url
        self.title = title
        self.link = link
        self.id = id
        self.author_name = author_name

    def download(self):
        pass
