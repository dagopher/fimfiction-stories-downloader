import fimfic
import pprint

session = fimfic.Session()
session.infodump()

URLs = [
    "http://www.fimfiction.net/bookshelf/1364962/xeno",
]

#"https://www.fimfiction.net/bookshelf/683004/favourites?page=7&&view_mode=1",

for url in URLs:
    print(f"URL: {url}")
    b = fimfic.Bookshelf(session=session,url=url)
    b.get_stories(single_page=True)
    b.infodump()
    print()

# vim: ts=4 sw=4 et tw=100 : 
