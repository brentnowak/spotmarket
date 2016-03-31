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
    print(kill)
    if kill != None:
        timestamp = str(kill['timestamp'])
        timestamp = timestamp.replace('"', '').replace('.', '-')
        timestamp = arrow.get(timestamp)
        print(type(timestamp))
        print(timestamp)
        insertkillmailsumrecord(kill['killID'], kill['characterid'], kill['corporationid'], kill['typeid'], kill['attackercount'], kill['damagetaken'], kill['timestamp'], kill['solarsystemid'], kill['x'], kill['y'], kill['z'])
    else:
        print("[km][empty JSON]")
    minkmid += 1

