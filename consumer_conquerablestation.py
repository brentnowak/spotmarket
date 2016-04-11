#-----------------------------------------------------------------------------
# consumer_conquerablestation.py
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

from time import sleep
from _meta import *
import evelink.eve
import sys
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()
#  Suppress InsecurePlatformWarning messages


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
    count_stationinsert = meta_insertconquerablestation(station_data)
    print(count_stationinsert)


if __name__ == "__main__":
    main()
    print("[Completed Run:Sleeping for 12 Hours]")
    sys.stdout.flush()
    sleep(43200)
