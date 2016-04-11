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
# Version: 0.3
# - Migrate to supervisor
#-----------------------------------------------------------------------------

import evelink.map
import sys
from _map import *
from time import sleep
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()
#  Suppress InsecurePlatformWarning messages

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
    count_mapinsert = map_insertkillsrecords(mapapi_data, killstimestamp)
    detail = "[map.kill] insert " + str(count_mapinsert) + " @ " + str(round(count_mapinsert/(time.time() - start_time), 2)) + " rec/sec"
    insertlog(service, 0, detail, killstimestamp)

    # Run Jumps import
    start_time = time.time()
    count_jumpsinsert = map_insertjumpsrecords(jumpsapi_data, jumpstimestamp)
    detail = "[map.jump] insert " + str(count_jumpsinsert) + " @ " + str(round(count_jumpsinsert/(time.time() - start_time), 2)) + " rec/sec"
    insertlog(service, 0, detail, jumpstimestamp)

    # Run Sov import
    start_time = time.time()
    count_sovinsert = map_insertsov(sovapi_data, sovtimestamp)
    detail = "[map.sov] insert " + str(count_sovinsert)  + " @ " + str(round(count_sovinsert/(time.time() - start_time), 2)) + " rec/sec"
    insertlog(service, 0, detail, sovtimestamp)

if __name__ == "__main__":
    main()

    # Sleep for 30 minutes before ending and triggering another run via supervisor
    print("[Completed Run:Sleeping for 30 Minutes]")
    sys.stdout.flush()
    sleep(1800)
