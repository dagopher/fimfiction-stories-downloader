import urllib.parse as urlparse
import pprint

from fimfic.ffobj import FimFicObj

class Bookshelf(FimFicObj):

    def __init__(self, session, url):

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


    def get_stories(self, single_page=False):
        soup = Soup(session=self.session, url=modified_url)

        while True:
            self.stories.append( soup.get_stories() )

            next_page_number = next_page_number(soup)

            if next_page_number:
                query_string['page'] = str(next_page_number)
                parsed_url[4] = urlparse.urlencode(query_string)
                next_url = urlparse.urlunparse(parsed_url)
                soup = Soup(session=self.session, url=next_url)
            else:
                break

# vim: ts=4 sw=4 et tw=100 :
