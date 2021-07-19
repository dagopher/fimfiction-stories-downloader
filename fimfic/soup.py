from fimfic.ffobj import FimFicObj
from bs4 import BeautifulSoup

def parse_storycard_container(storycard_container):
    story_link_container = storycard_container.find("a", class_='story_link')

    story_title = story_link_container.attrs["title"].encode('ascii', 'ignore'),
    story_link  = story_link_container.attrs["href"]
    story_id    = story_link.split("/")[2]

    story_data = {
        'author_name': storycard_container.find("a", class_='story-card__author').get_text(),
        'link': story_link,
        'title': story_title,
        'story_id': story_id,
    }

    return story_data

class Soup(FimFicObj):

    def __init__(self, session, *kwargs):
        self.session = session

        try:
            self.soup = BeautifulSoup( session.get(url).text , "lxml")
        except requests.exceptions.MissingSchema:
            raise FfsdError("Incorrect address. Check it for mistakes.\n"
                            "Remember that it has to start with 'https://www'. Try again.")


    def next_page_number(soup):
        """
        Return the page number of the next page in sequence.
        """
    
        # If there is a right chevron to "click for next page" then we know there is a next page
        if soup.find(class_='fa fa-chevron-right'):
            list_of_pages = soup.find(class_='page_list')  
            return int(list_of_pages.findAll('a', href=True)[-1].text)
        else:
            return None


    def get_storycards(self):
        return self.soup.findAll("div", class_='story-card-container')


    def get_stories(self):
        stories = []
        for sc in self.soup.findAll("div", class_='story-card-container'):
            stories.append( Story(parse_storycard_container(sc)) )

        return stories

# vim: ts=4 sw=4 et tw=100 : 
