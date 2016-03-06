from _utility import *

start_time = time.time()
service = "process_updatemoons.py"
moonInsertCount = 0

moons = getverifiedmoons()
for row in moons:
    moonID = row[0]
    typeID = row[1]
    moonInsertCount += updatemoonmineralstable(moonID, typeID)

timestamp = arrow.get() # Get arrow object
timestamp = timestamp.timestamp # Get timestamp of arrow object

detail = "[moonupdate] insert " + str(moonInsertCount) + " @ " + str(round(moonInsertCount/(time.time() - start_time), 3)) + " rec/sec"
insertlog_timestamp(service, 0, detail, timestamp)
