#-----------------------------------------------------------------------------
# consumer_alliance.sh
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

import evelink.eve
import sys
from time import sleep
from _alliances import *

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

    # Sleep for 30 minutes before ending and triggering another run via supervisor
    print("[Completed Run:Sleeping for 1 Hour]")
    sys.stdout.flush()
    sleep(3900)
