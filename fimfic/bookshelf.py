from urllib.parse import urlparse


class Bookshelf:
    def __init__(self, url):
        self.url = url
        self.parsed = urlparse(url)
        self.name = self.parsed.path.split("/")[-1]

        self.stories = []

    def load(self, session):
        session.cookies.jar.set('d_browse_bookshelf', '2')  # grid-like view
