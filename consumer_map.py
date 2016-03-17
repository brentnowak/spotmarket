#-----------------------------------------------------------------------------
# consumer_map.py
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
# Version: 0.11
# - Move configuration and functions to _utility.py
# Version: 0.2
# - Add Sovereignty
#-----------------------------------------------------------------------------

import evelink.map
from _utility import *

# API
killsapi = evelink.map.Map()
killsresponse = killsapi.kills_by_system()

jumpsapi = evelink.map.Map()
jumpresponse = jumpsapi.jumps_by_system()

sovapi = evelink.map.Map()
sovresponse = sovapi.sov_by_system()

# Convert timestamps to Arrow
killsapi_cachedUntil = arrow.get(killsresponse.expires)
jumps_cachedUntil = arrow.get(jumpresponse.expires)
sov_cachedUntil = arrow.get(sovresponse.expires)

# Format timestamps
killstimestamp = killsapi_cachedUntil.format('YYYY-MM-DD HH:mm:ss')
jumpstimestamp = jumps_cachedUntil.format('YYYY-MM-DD HH:mm:ss')
sovtimestamp = sov_cachedUntil.format('YYYY-MM-DD HH:mm:ss')

# Get dictionary
mapapi_data = killsresponse.result[0]
jumpsapi_data = jumpresponse.result[0]
sovapi_data = sovresponse.result[0]


def main():
    service = "consumer_map.py"

    # Run Kills import
    start_time = time.time()
    count_mapinsert = insertkillsrecords(mapapi_data, killstimestamp)
    detail = "[kills] insert " + str(count_mapinsert) + " @ " + str(round(count_mapinsert/(time.time() - start_time), 2)) + " rec/sec"
    insertlog(service, 0, detail, killstimestamp)

    # Run Jumps import
    start_time = time.time()
    count_jumpsinsert = insertjumpsrecords(jumpsapi_data, jumpstimestamp)
    detail = "[jumps] insert " + str(count_jumpsinsert) + " @ " + str(round(count_jumpsinsert/(time.time() - start_time), 2)) + " rec/sec"
    insertlog(service, 0, detail, jumpstimestamp)

    # Run Sov import
    start_time = time.time()
    count_sovinsert = insertsov(sovapi_data, sovtimestamp)
    detail = "[sov] insert " + str(count_sovinsert)  + " @ " + str(round(count_sovinsert/(time.time() - start_time), 2)) + " rec/sec"
    insertlog(service, 0, detail, sovtimestamp)

if __name__ == "__main__":
    main()
