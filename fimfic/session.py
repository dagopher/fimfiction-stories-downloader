import requests

class Session:
    def __init__(self):
        self = requests.Session()

        jar = requests.cookies.RequestsCookieJar()
        jar.set('view_mature', 'false')

        self.cookies = jar

    def enable_mature(self):
        self.cookies.jar.set('view_mature', 'true')
        
    def enable_mature(self):
        self.cookies.jar.set('view_mature', 'false')

# vim: ts=4 sw=4 et tw=100 : 
