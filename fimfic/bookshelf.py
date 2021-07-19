import urllib.parse as urlparse
import pprint

from fimfic.ffobj import FimFicObj

class Bookshelf(FimFicObj):
    def __init__(self, url):

        if 'fimfiction.net/story' in url:
            raise FfsdError(
                "This program cannot download single stories. You need the website address with a list of stories."
            )

        self.url = url
        self.parsed = urlparse.urlparse(url)
        self.name = self.parsed.path.split("/")[-1]
        self.stories = []

        # sometimes the cookie doesn't work, so force view mode in query string
        url_parts = list(self.parsed)
        query = dict(urlparse.parse_qsl(self.parsed.query))
        query.update({'view_mode': '2'})

        url_parts[4] = urlparse.urlencode(query)
        self.modified_url = urlparse.urlunparse(url_parts)


    def load_stories(self, session, page=None):
        session.cookies.jar.set('d_browse_bookshelf', '2')  # grid-like view

        modified_url, parsed_url, query_string = parse_bookshelf_url(bookshelf_url)
        current_page = int(query_string.get('page', '1'))

        soup = session.fetch_soup( url=modified_url )
        # print(soup.prettify().encode('ascii', 'ignore'))

        # it downloads the current page of stories from the 'popular stories', 'newest stories' etc.
        # it also prevents from downloading thousands of stories at once from the search results by accident
        if 'fimfiction.net/stories?' in url:
            end_page = current_page

        # Only want current page
        elif not all_pages:
            end_page = current_page

        else:
            end_page = range_of_pages(soup)

        print(f"CURRENT_PAGE: {current_page}, END_PAGE: {end_page}")

        stories = []

        while True:
            # print("looking for storycards")
            for storycard_container in soup.findAll("div", class_='story-card-container'):
                stories.append(parse_storycard_container(storycard_container))

            if current_page == end_page:
                break
            else:
                current_page += 1

                query_string['page'] = str(current_page)
                parsed_url[4] = urlparse.urlencode(query_string)
                next_page = urlparse.urlunparse(parsed_url)
                soup = get_the_website_data(url=next_page, session=session)

        return stories

# vim: ts=4 sw=4 et tw=100 :
