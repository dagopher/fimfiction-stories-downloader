from fimfic.ffobj import FimFicObj

import requests

class Session(FimFicObj):

    def __init__(self):
        session = requests.Session()

        session.cookies = requests.cookies.RequestsCookieJar()
        session.cookies.set('view_mature', 'false')

        self.session = session


    def enable_mature(self):
        self.session.cookies.set('view_mature', 'true')
        

    def disable_mature(self):
        self.session.cookies.set('view_mature', 'false')


    def set_cookie(self, key, value, *kwargs):
        self.session.cookies.set(key, value)

# vim: ts=4 sw=4 et tw=100 : 
