#-----------------------------------------------------------------------------
# consumer_markethistory.py - EVE Online CREST API consumer
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

import pycrest
import time
import arrow
from _utility import *


def main():
    eve = pycrest.EVE()

    regions = ['10000002', '10000043'] # The Forge, Domain
    typeIDs = getships()

    for regionID in regions:
        for typeID in typeIDs:
            start_time = time.time()
            url = "https://public-crest.eveonline.com/market/" + str(regionID) + "/types/" + str(typeID[0]) + "/history/"
            history = eve.get(url)
            count = insertmarket(regionID, typeID, history)
            timemark = arrow.get().to('US/Pacific').format('YYYY-MM-DD HH:mm:ss')
            print("[" + str(timemark) + "][consumer_markethistory.py][insert:" + str(count) + " @ " + str(round(count/(time.time() - start_time), 2)) + "rec/sec][regionID:" + str(regionID) + "][typeID:" + str(typeID[0]) + "]")


if __name__ == "__main__":
    main()