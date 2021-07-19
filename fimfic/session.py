import requests
from bs4 import BeautifulSoup

from fimfic.ffobj import FimFicObj

class Session(FimFicObj):
    def __init__(self):
        self = requests.Session()

        jar = requests.cookies.RequestsCookieJar()
        jar.set('view_mature', 'false')

        self.cookies = jar

    def enable_mature(self):
        self.cookies.jar.set('view_mature', 'true')
        
    def disable_mature(self):
        self.cookies.jar.set('view_mature', 'false')

    def fetch_soup(self, url):
        print(f"FETCHING URL: {url}")
        try:
            return BeautifulSoup( session.get(url).text , "lxml")
        except requests.exceptions.MissingSchema:
            raise FfsdError("Incorrect address. Check it for mistakes.\n"
                            "Remember that it has to start with 'https://www'. Try again.")

# vim: ts=4 sw=4 et tw=100 : 
