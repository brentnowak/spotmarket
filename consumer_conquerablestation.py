#-----------------------------------------------------------------------------
# consumer_conquerablestation.py - EVE Online XML API consumer
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

import evelink.eve
from _utility import *

# API
conquerablestationapi = evelink.eve.EVE()
stationresponse = conquerablestationapi.conquerable_stations()

# Get dictionary
station_data = stationresponse[0]

# Convert timestamps to Arrow
conquerablestationapi_cachedUntil = arrow.get(stationresponse.expires)

# Format timestamps
stationresponsetimestamp = conquerablestationapi_cachedUntil.format('YYYY-MM-DD HH:mm:ss')


def main():
    count_stationinsert = insertconquerablestations(station_data)
    print(count_stationinsert)


if __name__ == "__main__":
    main()