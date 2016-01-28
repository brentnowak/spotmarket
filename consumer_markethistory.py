#-----------------------------------------------------------------------------
# consumer_markethistory.py - EVE Online CREST API consumer
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

import pycrest
from _utility import *


def main():
    eve = pycrest.EVE()

    regions = ['10000002', '10000043'] # The Forge, Domain
    typeIDs = getships()

    for regionID in regions:
        for typeID in typeIDs:
            url = "https://public-crest.eveonline.com/market/" + str(regionID) + "/types/" + str(typeID[0]) + "/history/"
            history = eve.get(url)
            count = insertmarket(regionID, typeID, history)
            print("[Informational] Market Record Inserted: " + str(count))

if __name__ == "__main__":
    main()