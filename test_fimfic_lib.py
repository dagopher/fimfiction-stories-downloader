import fimfic
import pprint

session = fimfic.Session()
session.enable_mature()
session.infodump()
print("-------------")

URLs = [
    "http://www.fimfiction.net/bookshelf/1364962/xeno",
    "https://www.fimfiction.net/bookshelf/683004/favourites?view_mode=1",
]

#"https://www.fimfiction.net/bookshelf/683004/favourites?page=7&&view_mode=1",

for url in URLs:
    print(f"URL: {url}")
    b = fimfic.Bookshelf(session=session,url=url)
    s = b.load_stories(single_page=False)
    b.infodump()
    print("NUM STORIES FOUND: "  + str(len(s)))
    print()

# vim: ts=4 sw=4 et tw=100 :
