#-----------------------------------------------------------------------------
# consumer_siphon.py -
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------
#
# Input: None
# Output: Populate 'data.moonverify' table with a list of CREST verified moons.
# Right now it is using zKillboard as filter to find killmails for Siphon units and then uses the killID+Hash to look up the CREST killmail.
#-----------------------------------------------------------------------------

from _utility import *
import requests
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()
#  Suppress InsecurePlatformWarning messages

start_time = time.time()

pageNum = 1
while pageNum <= 1:
    url = 'https://zkillboard.com/api/losses/shipID/33477/orderDirection/desc/'
    headers = {'user-agent': 'github.com/brentnowak/spotmarket'}
    r = requests.get(url, headers=headers)

    service = "consumer_siphon.py"
    moonInsertCount = 0
    killmailInsertCount = 0

    for kill in json.loads(r.text):
        killID = kill['killID']
        killHash = kill['zkb']['hash']
        totalValue = kill['zkb']['totalValue']

        if checkforkillmail(killID, killHash) == False:  # Check if killmail exists, if not, fetch from CREST
            crestURL = 'https://public-crest.eveonline.com/killmails/' + str(killID) + '/' + str(killHash) + '/'
            print(crestURL)
            crestKill = requests.get(crestURL)
            data = json.loads(crestKill.text)

            solarSystemID = data.get('solarSystem', {'id': 'NA'})['id']
            try:
                typeID = data['victim']['items'][0]['itemType']['id']
            except IndexError: # Handle if no items are dropped
                typeID = None
            try:
                typeName = data['victim']['items'][0]['itemType']['name']
            except IndexError:
                typeName = None
            try:
                killx = data['victim']['position']['x']
            except KeyError: # Handle if killmail is pre-parallax (2015-11-03) and does not include x,y,z
                killx = None
            try:
                killy = data['victim']['position']['y']
            except KeyError:
                killy = None
            try:
                killz = data['victim']['position']['z']
            except KeyError:
                killz = None

            killmailInsertCount += insertkillmailrecord(killID, killHash, crestKill.text, totalValue)

            if killx != None:
                if typeID != None:
                    result = getclosestmoon(solarSystemID, killx, killy, killz)
                    moonID = result[3]
                    print(str(solarSystemID) + " : " + typeName + " - " + str(moonID))
                    print("Kill location: " + str(killx), str(killy), str(killz))
                    if insertmoonrecordverifygroup(typeID) == 501: #  Only moon minerals
                        moonInsertCount += insertmoonverifyrecord(moonID, killID, typeID)
        else:
            print("[skip][killID:" + str(killID) + "]")

    timestamp = arrow.get() # Get arrow object
    timestamp = timestamp.timestamp # Get timestamp of arrow object

    detail = "[killmail] insert " + str(killmailInsertCount) + " @ " + str(round(killmailInsertCount/(time.time() - start_time), 3)) + " rec/sec"
    insertlog_timestamp(service, 0, detail, timestamp)

    detail = "[moonverify] insert " + str(moonInsertCount) + " @ " + str(round(moonInsertCount/(time.time() - start_time), 3)) + " rec/sec"
    insertlog_timestamp(service, 0, detail, timestamp)

    print("Completed Page: " + str(pageNum))
    pageNum += 1
