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
        pass
