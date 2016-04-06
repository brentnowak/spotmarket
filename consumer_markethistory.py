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

import concurrent.futures
import multiprocessing
from time import sleep
from _market import *


maxWorkers = multiprocessing.cpu_count()  # Scale workers to machine size


def main():
    for regionID in regionIDs:
        currentItems = 1
        with concurrent.futures.ProcessPoolExecutor(max_workers=maxWorkers) as executor:
            future_to_typeid = {executor.submit(market_getcrestdata, regionID[0], typeID[0]): typeID[0] for typeID in typeIDs}
            for future in concurrent.futures.as_completed(future_to_typeid):
                currentItems += 1
    market_setimportresult(regionID[0], 1)  # Set import to true so we can skip this region if we crash


if __name__ == "__main__":
    typeIDs = market_typeids()
    regionIDs = market_regionids()

    main()

    print("[Completed Run:Sleeping for 1 Hour]")
    sys.stdout.flush()
    sleep(3600)
