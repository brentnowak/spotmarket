#-----------------------------------------------------------------------------
# consumer_xml.py - EVE Online XML API consumer
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
# Version: 0.11
# - Move configuration and functions to _utility.py
#-----------------------------------------------------------------------------

import evelink.map
from _utility import *

# API
mapapi = evelink.map.Map()
mapresponse = mapapi.kills_by_system()

jumpsapi = evelink.map.Map()
jumpresponse = jumpsapi.jumps_by_system()

sovapi = evelink.map.Map()
sovresponse = sovapi.sov_by_system()

# Convert timestamps to Arrow
mapapi_cachedUntil = arrow.get(mapresponse.expires)
jumps_cachedUntil = arrow.get(jumpresponse.expires)
sov_cachedUntil = arrow.get(sovresponse.expires)

# Format timestamps
maptimestamp = mapapi_cachedUntil.format('YYYY-MM-DD HH:mm:ss')
jumpstimestamp = jumps_cachedUntil.format('YYYY-MM-DD HH:mm:ss')
sovtimestamp = sov_cachedUntil.format('YYYY-MM-DD HH:mm:ss')

# Get dictionary
mapapi_data = mapresponse.result[0]
jumpsapi_data = jumpresponse.result[0]
sovapi_data = sovresponse.result[0]


def main():
    service = "consumer_xml.py"

    # Run Map import
    count_mapinsert = insertmap(mapapi_data, maptimestamp)
    detail = "[map] insert " + str(count_mapinsert)
    print(detail)
    insertlog(service, 0, detail, maptimestamp)

    # Run Jumps import
    count_jumpsinsert = insertjumps(jumpsapi_data, jumpstimestamp)
    detail = "[jump] insert " + str(count_jumpsinsert)
    print(detail)
    insertlog(service, 0, detail, jumpstimestamp)

    # Run Sov import
    count_sovinsert = insertsov(sovapi_data, sovtimestamp)
    detail = "[sov] insert " + str(count_sovinsert)
    print(detail)
    insertlog(service, 0, detail, sovtimestamp)

if __name__ == "__main__":
    main()


