#-----------------------------------------------------------------------------
# consumer_markethistory.py -
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------
#
# Input: List of typeIDs from 'data.marketitems' table that have 'enabled' set to 1.
# Output: Populate 'data.markethistory' table. Prices are currenlty only set for the Forge.
#-----------------------------------------------------------------------------

from _utility import *
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
            currentItem += 1
        currentRegion += 1

if __name__ == "__main__":
    main()
