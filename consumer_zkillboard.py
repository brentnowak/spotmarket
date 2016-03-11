from _utility import *
from requests.exceptions import ConnectionError

#############################
#
# Work in progress
#
#############################

# 20183  Providence
# 20185  Charon
# 20187  Obelisk
# 20189  Fenrir

ships = getzkbships()

for ship in ships:
    start_time = time.time()
    url = 'https://zkillboard.com/api/losses/shipID/' + str(ship[0]) + '/orderDirection/desc/'
    headers = {'user-agent': 'github.com/brentnowak/spotmarket'}
    r = requests.get(url, headers=headers)

    service = "consumer_zkillboard.py"
    killmailInsertCount = 0

    for kill in json.loads(r.text):
        killID = kill['killID']
        killHash = kill['zkb']['hash']
        crestURL = 'https://public-crest.eveonline.com/killmails/' + str(killID) + '/' + str(killHash) + '/'
        print(crestURL)
        try:
            crestKill = requests.get(crestURL)
        except ConnectionError as e:
            print(e)
        else:
            data = json.loads(crestKill.text)

            killmailInsertCount += insertkillmailrecord(killID, killHash, crestKill.text)

    timestamp = arrow.get() # Get arrow object
    timestamp = timestamp.timestamp # Get timestamp of arrow object

    detail = "[zkb][typeID:" + str(ship[0]) + "] insert " + str(killmailInsertCount) + " @ " + str(round(killmailInsertCount/(time.time() - start_time), 3)) + " rec/sec"
    insertlog_timestamp(service, 0, detail, timestamp)
