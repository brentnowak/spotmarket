#-----------------------------------------------------------------------------
# consumer_zkillboard.py -
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release.
# Version: 0.2
# - Loop over ships from data.killmailsitems table, zkillboard paging, basic requests exception handling.
#-----------------------------------------------------------------------------
#
# Input: List of ships from data.killmailsitems table.
# Output: Populate 'data.killmails' table with a list of CREST verified killmails.
# Use zKillboard as filter to find killmails and then use killID+Hash to look up the CREST killmail.
# Store CREST JSON to table along with zKillboard value.
#-----------------------------------------------------------------------------

import sys
from _utility import *
from _consumer_kills import *
from requests.exceptions import ConnectionError, ChunkedEncodingError
from time import sleep
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()
#  Suppress InsecurePlatformWarning messages

ships = getzkbships()
#  Get list of typeIDs that have 'enabled' set to 1

for typeID in ships:
    pageNum = 1
    if getzkbpagenumber(typeID[0]) != pageNum:  #  Pick up state and start at last page-1
        pageNum = getzkbpagenumber(typeID[0])-1
    r = requests.Response() #  Init requests for new ship after we have finished a specific typeID

    while r.text != "[]":
        start_time = time.time()
        service = "consumer_zkillboard.py"
        killmailInsertCount = 1

        url = 'https://zkillboard.com/api/losses/shipID/' + str(typeID[0]) + '/orderDirection/desc/page/' + str(pageNum) + "/"
        headers = {'user-agent': 'github.com/brentnowak/spotmarket'}

        try:
            r = requests.get(url, headers=headers)
        except (ConnectionError, ChunkedEncodingError) as e:
            print(e)
        else:
            for kill in json.loads(r.text):
                killID = kill['killID']
                killHash = kill['zkb']['hash']
                killTime = kill['killTime']
                solarSystemID = kill['solarSystemID']
                totalValue = kill['zkb']['totalValue']

                if checkforkillmail(killID, killHash) == False:  # Check if killmail exists, if not, fetch from CREST
                    crestURL = 'https://public-crest.eveonline.com/killmails/' + str(killID) + '/' + str(killHash) + '/'
                    print("[" + str(gettypeName(typeID[0])) + "][page:" + str(pageNum) + "][count:" + str(killmailInsertCount) + "][killTime:" + str(killTime) + "][killID:" + str(killID) + "][solarSystemName:" + str(getSolarSystemName(solarSystemID)) + "]")  # Feedback
                    sys.stdout.flush()
                    try:
                        crestKill = requests.get(crestURL)
                    except (ConnectionError, ChunkedEncodingError) as e:
                        print(e)
                    else:
                        killmailInsertCount += insertkillmailrecord(killID, killHash, crestKill.text, totalValue)
                else:
                    print("[" + str(gettypeName(typeID[0])) + "][skip][killID:" + str(killID) + "]")
                    sys.stdout.flush()

            timestamp = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss')  # Get UTC arrow object
            detail = "[zkb][typeID:" + str(typeID[0]) + "] insert " + str(killmailInsertCount - 1) + " @ " + str(round((killmailInsertCount - 1) / (time.time() - start_time), 3)) + " rec/sec"
            insertlog_timestamp(service, 0, detail, timestamp)
            setzkblastpage(typeID[0], pageNum)  # Keep track of paging
            print("----------------------")
            print("[Completed Page:" + str(pageNum) + "]")
            print("----------------------")
            sys.stdout.flush()
            pageNum += 1

    # Record state to data.killmailsitems because we're done with a specific typeID
    setzkbshipenable(typeID[0], 0)  # Successful run sets enabled to 0
    setzkbshipresult(typeID[0], 1)  # Successful run sets importResult to 1

    # Be nice to squizz and sleep for 5 seconds before requesting another 200 KMs
    print("----------------------")
    print("[Completed Ship:" + str(gettypeName(typeID[0])) + "]")
    print("----------------------")
    sys.stdout.flush()
    sleep(5)

# Sleep for 1 hour before ending and triggering another run via supervisor
print("----------------------")
print("[Completed Run:Sleeping for 1 Hour]")
print("----------------------")
sys.stdout.flush()
sleep(3600)
