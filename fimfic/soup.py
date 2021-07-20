import requests
import urllib.parse as urlparse
from bs4 import BeautifulSoup

from fimfic.const import *
from fimfic.ffobj import FimFicObj
from fimfic.story import Story

def text_sanitize(txt):
    return txt.encode("latin-1").decode("utf-8")


def parse_storycard_container(storycard_container):
    story_link_container = storycard_container.find("a", class_='story_link')

    link = story_link_container.attrs["href"]

    story_data = {
        'author_name': text_sanitize(storycard_container.find("a", class_='story-card__author').get_text()),
        'url': URL_PREFIX + link,
        'title': text_sanitize(story_link_container.attrs["title"]),
        'id': link.split("/")[2]
    }

    return story_data

class Soup(FimFicObj):

    def __init__(self, session, url, **kwargs):
        self.session = session
        self.url = url
        self.fetch_data()


    def fetch_data(self, **kwargs):
        try:
            self.soup = BeautifulSoup( self.session.session.get(self.url).text , "lxml")
        except requests.exceptions.MissingSchema:
            raise FfsdError("Incorrect address. Check it for mistakes.\n"
                            "Remember that it has to start with 'https://www'. Try again.")


    def next_page_number(self, **kwargs):
        """
        Return the page number of the next page in sequence.
        """

        # If there is a right chevron to "click for next page" then we know there is a next page
        if self.soup.find(class_='fa fa-chevron-right'):
            page_list = self.soup.find('div', class_='page_list')
            chevron_href = page_list.findAll('a', href=True)[-1].attrs["href"]
            parsed = urlparse.urlparse(chevron_href)
            query = dict(urlparse.parse_qsl(parsed.query))
            return str(query['page'])
        else:
            return None


#    def get_storycards(self, **kwargs):
#        return self.soup.findAll("div", class_='story-card-container')


    def get_stories(self, **kwargs):
        stories = []
        for sc in self.soup.findAll("div", class_='story-card-container'):
            # Reminder to self, '**blah' expands dict into key/val arguments
            stories.append(Story( **parse_storycard_container(sc) ))

        import pprint
        print("STORY DATA: " + pprint.pformat(stories))
        for s in stories:
            s.infodump()
        return stories

# vim: ts=4 sw=4 et tw=100 :
