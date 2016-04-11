#
# Input     moonverify moonID, typeID
#           moonevemoons moonID, typeID
# Output    moonminerlas monID, typeID
#

import sys
import random
from _utility import *
from time import sleep

def main():
    start_time = time.time()
    service = "process_updatemoons.py"
    moonInsertCount = 0

    moons = getverifiedmoonscrest()
    for row in moons:
        moonID = row[0]
        typeID = row[1]
        moonInsertCount += updatemoonmineralstable(moonID, typeID)

    timestamp = arrow.get() # Get arrow object
    timestamp = timestamp.timestamp # Get timestamp of arrow object

    detail = "[moonupdate] insert " + str(moonInsertCount) + " @ " + str(round(moonInsertCount/(time.time() - start_time), 3)) + " rec/sec"
    insertlog_timestamp(service, 0, detail, timestamp)

    moons = getverifiedmoonsevemoons()
    for row in moons:
        moonID = row[0]
        typeID = row[1]
        moonInsertCount += updatemoonmineralstable(moonID, typeID)

    timestamp = arrow.get() # Get arrow object
    timestamp = timestamp.timestamp # Get timestamp of arrow object

    detail = "[moonupdate] insert " + str(moonInsertCount) + " @ " + str(round(moonInsertCount/(time.time() - start_time), 3)) + " rec/sec"
    insertlog_timestamp(service, 0, detail, timestamp)


if __name__ == "__main__":
    main()

    print("[Completed Run:Sleeping for 24 Hours]")
    sys.stdout.flush()
    sleep(86400 + random.randrange(0, 600))
