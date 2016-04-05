#-----------------------------------------------------------------------------
# consumer_markethistory.py -
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
# Version: 0.2
# - Migration to market.history
#-----------------------------------------------------------------------------
#
# Input: List of typeIDs from 'market.tracking' table that have 'enabled' set to 1.
# Output: Populate 'market.history' table.
#-----------------------------------------------------------------------------

import sys
from time import sleep
from _market import *
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()
#  Suppress InsecurePlatformWarning messages


def main():
    typeIDs = market_typeids()
    regionIDs = market_regionids()

    totalItems = float(len(typeIDs))
    currentItem = float(1)

    totalRegions = float(len(regionIDs))
    currentRegion = float(1)

    for regionID in regionIDs:
        for typeID in typeIDs:
            count = market_getcrestdata(regionID[0], typeID[0])
            itemProgress = str("{0:.2f}".format(currentItem/totalItems*100)) + "%"
            regionProgress = str("{0:.2f}".format(currentRegion/totalRegions*100)) + "%"
            print("[regionID:" + str(regionID[0]) + "," + regionProgress + "][" + str(getregionName(regionID[0])) + "][typeID:" + str(typeID[0]) + "," + itemProgress + "][insert:" + str(count) + "][" + str(gettypeName(typeID[0])) + "]")
            sys.stdout.flush()
            currentItem += 1
        currentRegion += 1
        market_setimportresult(regionID[0], 1)  # Set import to true so we can skip this region if we crash

    print("[Completed Run:Sleeping for 1 Hour]")
    sys.stdout.flush()
    sleep(3600)

if __name__ == "__main__":
    main()
