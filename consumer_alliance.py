#-----------------------------------------------------------------------------
# consumer_alliance.py - EVE Online XML API consumer
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

import evelink.eve
from _utility import *

# API
allianceapi = evelink.eve.EVE()
allianceresponse = allianceapi.alliances()

# Get dictionary
alliance_data = allianceresponse[0]


def main():
    count_allianceinsert = insertalliancesrecords(alliance_data)
    print(count_allianceinsert)


if __name__ == "__main__":
    main()