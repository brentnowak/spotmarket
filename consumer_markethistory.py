#-----------------------------------------------------------------------------
# consumer_markethistory.py - EVE Online CREST API consumer
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

from _utility import *


def main():

    # The Forge
    regionIDs = ['10000002']

    #1041	Advanced Commodities

    getmarkethistory(regionIDs)


if __name__ == "__main__":
    main()