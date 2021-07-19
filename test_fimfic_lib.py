import fimfic
import pprint

session = fimfic.Session()
session.infodump()

URLs = [
    "http://www.fimfiction.net/bookshelf/1364962/xeno",
    "https://www.fimfiction.net/bookshelf/683004/favourites?page=7&&view_mode=1",
    ]

for url in URLs:
    b = fimfic.Bookshelf(url=url)
    b.infodump()

# vim: ts=4 sw=4 et tw=100 : 
