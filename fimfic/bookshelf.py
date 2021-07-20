import urllib.parse as urlparse
import pprint

from fimfic.ffobj import FimFicObj
from fimfic.soup import Soup

class Bookshelf(FimFicObj):

    def __init__(self, session, url, **kwargs):

        if not url:
            raise("NO URL DEFINED")

        if not session:
            raise("NO SESSION DEFINED")

        if 'fimfiction.net/story' in url:
            raise FfsdError(
                "This program cannot download single stories. You need the website address with a list of stories."
            )

        self.url = url
        self.parsed = urlparse.urlparse(url)
        self.name = self.parsed.path.split("/")[-1]
        self.stories = []
        self.session = session
        self.session.set_cookie(key="d_browse_bookshelf", value="2")  # grid-like view

        # sometimes the cookie doesn't work, so force view mode in query string
        query = dict(urlparse.parse_qsl(self.parsed.query))
        query.update({'view_mode': '2'})

        url_parts = list(self.parsed)
        url_parts[4] = urlparse.urlencode(query)

        self.modified_url = urlparse.urlunparse(url_parts)


    def get_stories(self):
        return self.stories


    def load_stories(self, single_page=False, **kwargs):
        self.infodump()
        soup = Soup(session=self.session, url=self.modified_url)

        while True:
            # print(f"CURRENT URL: {soup.url}")
            self.stories.extend( soup.get_stories() )

            next_page_number = soup.next_page_number()

            if single_page:
                break
            elif next_page_number:
                query = dict(urlparse.parse_qsl(self.parsed.query))
                query.update({'page': str(next_page_number) })

                url_parts = list(self.parsed)
                url_parts[4] = urlparse.urlencode(query)

                next_url = urlparse.urlunparse(url_parts)
                soup = Soup(session=self.session, url=next_url)
            else:
                break

        return self.get_stories()


    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url,
            "stories": [ s.to_dict() for s in self.stories ],
        }


    def to_json(self):
        return FimFicObj.to_json(self, self.to_dict())
        
# vim: ts=4 sw=4 et tw=100 :
