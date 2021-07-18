import fimfic
import pprint

session = fimfic.Session()
print(pprint.pformat(session))

b = fimfic.Bookshelf(
        url="http://www.fimfiction.net/bookshelf/1364962/xeno"
    )

print(b.name)

# vim: ts=4 sw=4 et tw=100 : 
