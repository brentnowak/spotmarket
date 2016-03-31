#
# Input     CEST kills from
#           data.killmails
# Output
#

from _consumer_kills import *

maxkmid = getmaxkmid()
minkmid = getminkmid()

while minkmid <= maxkmid:
    killID = getkillid(minkmid)
    kill = getkmdetails(killID)
    if kill != None:
        timestamp = str(kill['timestamp'])
        timestamp = timestamp.replace('"', '').replace('.', '-')
        timestamp = arrow.get(timestamp)
        progress = str("{0:.3f}".format(float(minkmid) / float(maxkmid) * 100)) + "%"
        print("[" + str(progress) + "][killID:" + str(kill['killID']) + "][insert]")
        insertkillmailsumrecord(kill['killID'], kill['characterid'], kill['corporationid'], kill['typeid'], kill['attackercount'], kill['damagetaken'], kill['timestamp'], kill['solarsystemid'], kill['x'], kill['y'], kill['z'])
    else:
        print("[" + str(progress) + "][killID:" + str(kill['killID']) + "][empty JSON]")
    minkmid += 1
