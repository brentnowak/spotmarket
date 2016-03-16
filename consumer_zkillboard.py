#-----------------------------------------------------------------------------
# consumer_zkillboard.py -
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------
#
# Input: None
# Output: Populate 'data.killmails' table with a list of CREST verified killmails.
# Right now it is using zKillboard as filter to find killmails and then uses the killID+Hash to look up the CREST killmail.
#-----------------------------------------------------------------------------

from _utility import *
from requests.exceptions import ConnectionError, ChunkedEncodingError
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()
#  Suppress InsecurePlatformWarning messages

pageNum = 1
ships = getzkbships()
r = requests.Response()

for ship in ships:
    while r.text != "[]":
        start_time = time.time()
        url = 'https://zkillboard.com/api/losses/shipID/' + str(ship[0]) + '/orderDirection/desc/page/' + str(pageNum) + "/"
        headers = {'user-agent': 'github.com/brentnowak/spotmarket'}
        r = requests.get(url, headers=headers)

        service = "consumer_zkillboard.py"
        killmailInsertCount = 1

        for kill in json.loads(r.text):
            killID = kill['killID']
            killHash = kill['zkb']['hash']
            totalValue = kill['zkb']['totalValue']

            if checkforkillmail(killID, killHash) == False:  # Check if killmail exists, if not, fetch from CREST
                crestURL = 'https://public-crest.eveonline.com/killmails/' + str(killID) + '/' + str(killHash) + '/'
                print("[" + str(gettypeName(ship[0])) + "][count:" + str(killmailInsertCount) + "] " + crestURL) #  Feedback
                try:
                    crestKill = requests.get(crestURL)
                except (ConnectionError, ChunkedEncodingError) as e:
                    print(e)
                else:
                    killmailInsertCount += insertkillmailrecord(killID, killHash, crestKill.text, totalValue)
            else:
                print("[" + str(gettypeName(ship[0])) + "][skip][killID:" + str(killID) + "]")

        timestamp = arrow.utcnow()  # Get arrow object
        timestamp = timestamp.timestamp  # Get timestamp of arrow object

        detail = "[zkb][typeID:" + str(ship[0]) + "] insert " + str(killmailInsertCount-1) + " @ " + str(round((killmailInsertCount-1)/(time.time() - start_time), 3)) + " rec/sec"
        insertlog_timestamp(service, 0, detail, timestamp)

        print("Completed Page: " + str(pageNum))
        pageNum += 1

    setzkbshipenable(ship[0], 0)  # Successful API sets enabled to false
    setzkbshipresult(ship[0], 1)  # Successful API sets importResult to true
