#-----------------------------------------------------------------------------
# consumer_markethistory.py -
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
# Version: 0.2
# - Migration to market.history
# Version: 0.3
# - Migration to concurrent.futures
#-----------------------------------------------------------------------------
#
# Input: List of typeIDs from 'market.tracking' table that have 'enabled' set to 1.
# Output: Populate 'market.history' table.
#-----------------------------------------------------------------------------

import sys
import concurrent.futures
from time import sleep
from _market import *
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()
#  Suppress InsecurePlatformWarning messages

def main():
    for regionID in regionIDs:
        with concurrent.futures.ProcessPoolExecutor(max_workers=15) as executor:
            for typeID in typeIDs:
                executor.submit(market_getcrestdata, regionID[0], typeID[0])
                print("[regionID:" + str(regionID[0]) + "," + str(getregionName(regionID[0])) + "][typeID:" + str(
                    typeID[0]) + "][" + str(gettypeName(typeID[0])) + "]")
                sys.stdout.flush()

    market_setimportresult(regionID[0], 1)  # Set import to true so we can skip this region if we crash


if __name__ == "__main__":
    typeIDs = market_typeids()
    regionIDs = market_regionids()
    totalItems = float(len(typeIDs))
    totalRegions = float(len(regionIDs))

    main()

    print("[Completed Run:Sleeping for 1 Hour]")
    sys.stdout.flush()
    sleep(3600)
