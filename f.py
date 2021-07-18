import argparse
from bs4 import BeautifulSoup
import requests
import re
import os
import os.path
import sys
import urllib.parse as urlparse
import pprint


def main_program():

    format_choices = {
        'txt':  '1',
        'html': '2',
        'epub': '3',
    }

    url_prefix = 'https://www.fimfiction.net'

    class FfsdError(Exception):
        pass


    def create_download_folder(download_path):
        """
        Create a download folder if it does not exist
        """
        try:
            os.mkdir(download_path)
        except FileExistsError:
            pass

    def parse_bookshelf_url(url):
        """
        Get the url from a user and store the url for further use
        """
        print("Bookshelf URL:", url)

        if 'fimfiction.net/story' in url:
            raise FfsdError(
                "This program cannot download single stories. You need the website address with a list of stories."
            )

        parsed = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(parsed[4]))  # 4 as an equivalent to parsed_url.query
        query['view_mode'] = '2'                     # sometimes the cookie doesn't work, so double tap it
        parsed[4] = urlparse.urlencode(query)
        normalized_url = urlparse.urlunparse(parsed)

        print(f"\tPARSING BOOKSHELF URL: {url}")
        print(f"\tPARSED URL: {parsed}")
        print(f"\tURL QUERY: {query}")

        return normalized_url, parsed, query

    def establish_a_session():
        """
        Create a session with cookies
        """
        new_session = requests.Session()

        jar = requests.cookies.RequestsCookieJar()
        jar.set('view_mature', 'true' if named_args.adult else 'false')
        jar.set('d_browse_bookshelf', '2')  # grid-like view

        new_session.cookies = jar
        return new_session

    def get_the_website_data(url,session):
        """
        Get the source code of a website and check if the address is correct
        """
        print(f"FETCHING URL: {url}")
        try:
            source = session.get(url).text
        except requests.exceptions.MissingSchema:
            raise FfsdError("Incorrect address. Check it for mistakes.\n"
                            "Remember that it has to start with 'https://www'. Try again.")
        return BeautifulSoup(source, "lxml")


    def get_bookshelf_name(bookshelf_url):
        parsed = urlparse.urlparse(bookshelf_url)
        name = parsed.path.split("/")[-1]
        return name


    def parse_storycard_container(storycard_container):
        # print("found storycard")
        # print(storycard_container.prettify().encode('ascii', 'ignore'))

        story_link_container = storycard_container.find("a", class_='story_link')
        # print(story_link_container.prettify().encode('ascii', 'ignore'))

        print(type(story_link_container.attrs["title"]))
        story_title = story_link_container.attrs["title"].encode('ascii', 'ignore'),
        print(f"STORY TITLE: {story_title}")
        story_link  = story_link_container.attrs["href"]
        story_id    = story_link.split("/")[2]
        print(f"STORY ID: {story_id}")

        story_data = {
            'author_name': storycard_container.find("a", class_='story-card__author').get_text(),
            'link': story_link,
            'title': story_title,
            'story_id': story_id,
            'download_url_prefix': f"{url_prefix}/story/download/{story_id}/",
            'story_url': f"{url_prefix}{story_link}"
        }

        print("STORY DATA: " + pprint.pformat(story_data))
        return story_data


    def range_of_pages(soup):
        """
        Get the current page and the total number of pages. If there is more than one page, you can choose the range.
        """

        # No "right" chevron; must be last page
        if not soup.find(class_='fa fa-chevron-right'):
            end_page = current_page

        # Grab everything
        else:
            list_of_pages = soup.find(class_='page_list')  # more than one page and not the last page
            end_page = int(list_of_pages.findAll('a', href=True)[-2].text)

        return end_page


    def read_bookshelf(bookshelf_url, session, all_pages=True):
        """
        Get links to stories from a page and move to the next ones
        """

        normalized_url, parsed_url, query_string = parse_bookshelf_url(bookshelf_url)

        soup = get_the_website_data(url=normalized_url, session=session)
        # print(soup.prettify().encode('ascii', 'ignore'))

        current_page = int(query_string.get('page', '1'))

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

    def get_context_filename(file_data):
        """
        Get filename from content-disposition
        """
        cd = file_data.headers.get('content-disposition')

        if not cd:
            return None

        fetched_name = re.findall('filename=(.+)', cd)

        if len(fetched_name) == 0:
            return None

        filename = fetched_name[0].encode('latin-1').decode('utf-8')

        try:
            return eval(filename.rstrip(';'))
        except SyntaxError:
            return filename

    def check_filepath(path, story_id):
        if os.path.exists(path):
            in_id = path.rfind('.')
            return path[:in_id] + '_' + story_id + path[in_id:] if in_id != -1 else path + '_' + story_id
        return path

    def get_story_download_url(story_data,output_format):
        url = f"{story_data['download_url_prefix']}{output_format}"
        print(f"DOWNLOAD URL: {url}")
        return url

    def save_story(story_data,output_format,download_path):
        """
        Save the stories
        """
        translator = {'/': ''}

        download_url = get_story_download_url(story_data, output_format)
        fetched_file = session.get(download_url, allow_redirects=True)

        filename = get_context_filename(fetched_file)

        if not filename:
            filename = f"{story_data['story_id']}.{output_format}"  # fallback to 'id.ext'

        # TODO: Sanitize author_name to avoid nasty surprises in pathing
        download_directory = f"{download_path}/{story_data['author_name']}"
#        create_download_folder(download_directory)

        stripped_filename = filename.translate(str.maketrans(translator))
        download_path = check_filepath(os.path.join(download_directory, stripped_filename), story_data['story_id'])

#        with open(download_path, 'wb') as file:
#            file.write(fetched_file.content)
#            print(f"Wrote {download_path}")

    def sort_stories_by_author_title(list_of_stories):
        return sorted(list_of_stories, key=lambda k: (k['author_name'], k['title']))

    def write_bookshelf_report(list_of_stories):
        for s in list_of_stories:
            print(f"HERE: {s['author_name']},{s['title']},{s['story_id']},{s['story_url']}")

    # -----------------------------------------------------------------------

    default_out_dir = 'downloaded_stories'

    cla_parser = argparse.ArgumentParser()

    cla_parser.add_argument('-o', '--out', default=default_out_dir,
                            help='set the directory to which all stories will be downloaded '
                                 f"(default is {default_out_dir})")

    cla_parser.add_argument('-a', '--adult', default=False, action='store_true',
                            help='Enable downloading of mature rated stories (default is to not do this)')

    cla_parser.add_argument('-f', '--format', choices=format_choices.keys(),
                            help='set the file format for all downloaded stories')

    cla_parser.add_argument('-r', '--range', choices=['1', '2'],
                            help='set whether to download only from the current page (1) '
                                 'or from all pages starting with the current one (2)')

    cla_parser.usage = __file__ + ' [options] [URLs]'

    cla_parser.epilog = "If any numbers of URLs are passed, the program will process them and quit. Otherwise " \
                        "it'll ask the user to input them until an interrupt signal or EOF is encountered." \
                        "If the rating, format or range isn't passed, the user will be asked to specify the " \
                        "missing settings for each URL."

    named_args,urls = cla_parser.parse_known_args()

    print("ARGS: " + pprint.pformat(named_args))
    print("URLS: " + pprint.pformat(urls))

    # -----------------------------------------------------------------------
    # Parameter validation
    # -----------------------------------------------------------------------

    if not urls:
        sys.stderr.write('No URLs defined')
        cla_parser.print_help()
        sys.exit(2)

    if named_args.format not in format_choices.keys():
        sys.stderr.write('Output format not defined')
        cla_parser.print_help()
        sys.exit(2)

    if not named_args.range:
        sys.stderr.write("Page range target not defined")
        cla_parser.print_help()
        sys.exit(2)

    # -----------------------------------------------------------------------

    # TODO: should only create directory if user actually wants to download stuff
    create_download_folder(named_args.out)

    session = establish_a_session()

    for url in urls:
        try:
            print("BOOKSHELF NAME: " + get_bookshelf_name(bookshelf_url=url))

            all_stories = read_bookshelf(
                session=session,
                bookshelf_url=url,
            )

            all_stories = sort_stories_by_author_title(all_stories)

            # TODO: this should be optional
            write_bookshelf_report(all_stories)

            # TODO: only write if triggered with command-line option
#            for s in (all_stories):
#                save_story(story_data=s,output_format=named_args.format,download_path=named_args.out)

        except FfsdError as err:
            print(err)

if __name__ == "__main__":
    main_program()
