#-----------------------------------------------------------------------------
# consumer.py - EVE Online API consumer
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 1.0
# - Initial release
# Version: 1.1
# - Remove record check function before INSERT
# - Move configuration and functions to _utility.py
#-----------------------------------------------------------------------------

import arrow
import evelink.map

from _utility import *

# API
mapapi = evelink.map.Map()
mapresponse = mapapi.kills_by_system()
jumpsapi = evelink.map.Map()
jumpresponse = jumpsapi.jumps_by_system()

# Convert timestamps to Arrow
mapapi_cachedUntil = arrow.get(mapresponse.expires)
jumps_cachedUntil = arrow.get(jumpresponse.expires)

# Get dictionary
mapapi_data = mapresponse.result[0]
jumpsapi_data = jumpresponse.result[0]

# Format timestamps
maptimestamp = mapapi_cachedUntil.format('YYYY-MM-DD HH:mm:ss')
jumpstimestamp = jumps_cachedUntil.format('YYYY-MM-DD HH:mm:ss')


def main():
    # Run Map import
    count_mapinsert = insertmap(mapapi_data)
    print("[" + str(maptimestamp) + "][Informational] Map Inserted: " + str(count_mapinsert))

    # Run Jumps import
    count_jumpsinsert = insertjumps(jumpsapi_data)
    print("[" + str(jumpstimestamp) + "][Informational] Jumps Inserted: " + str(count_jumpsinsert))


if __name__ == "__main__":
    main()


