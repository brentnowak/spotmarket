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

import concurrent.futures
import multiprocessing
import requests.packages.urllib3
from _kills import *
from time import sleep
from requests.exceptions import ConnectionError, ChunkedEncodingError

requests.packages.urllib3.disable_warnings()
maxWorkers = multiprocessing.cpu_count()  # Scale workers to machine size


def main():
    for typeID in ships:
        pageNum = 1
        if getzkbpagenumber(typeID[0]) != pageNum:  #  Pick up state and start at last page-1 to handle crashes
            pageNum = getzkbpagenumber(typeID[0])-1
        r = requests.Response() #  Init requests for new ship after we have finished a specific typeID

        while r.text != "[]":
            start_time = time.time()
            service = "consumer_zkillboard.py"

            url = 'https://zkillboard.com/api/losses/shipID/' + str(typeID[0]) + '/orderDirection/desc/page/' + str(pageNum) + "/"
            headers = {'user-agent': 'github.com/brentnowak/spotmarket'}
            try:
                r = requests.get(url, headers=headers)
            except (ConnectionError, ChunkedEncodingError, ValueError) as e:
                print(e)
            else:
                killmailInsertCount = 1
                with concurrent.futures.ProcessPoolExecutor(max_workers=maxWorkers) as executor:
                    future_to_killid = {executor.submit(kills_getcrestdata, typeID[0], pageNum, kill['killID'], kill['zkb']['hash'], kill['killTime'], kill['solarSystemID'], kill['zkb']['totalValue']): kill['killID'] for kill in json.loads(r.text)}
                    for future in concurrent.futures.as_completed(future_to_killid):
                        killmailInsertCount += 1

                timestamp = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss')  # Get UTC arrow object
                detail = "[zkb][typeID:" + str(typeID[0]) + "] insert " + str(killmailInsertCount - 1) + " @ " + str(round((killmailInsertCount - 1) / (time.time() - start_time), 3)) + " rec/sec"
                insertlog_timestamp(service, 0, detail, timestamp)
                setzkblastpage(typeID[0], pageNum)  # Keep track of paging
                print("[Completed Page:" + str(pageNum) + "]")
                sys.stdout.flush()
                pageNum += 1
                sleep(10)  # Be nice to squizz and sleep before requesting another 200 KMs

        # Record state to data.killmailsitems because we're done with a specific typeID
        setzkbshipenable(typeID[0], 0)  # Successful run sets enabled to 0
        setzkbshipresult(typeID[0], 1)  # Successful run sets importResult to 1

        print("[Completed Ship:" + str(gettypeName(typeID[0])) + "]")
        sys.stdout.flush()
        sleep(1)  # Be nice to squizz and sleep before requesting another 200 KMs


if __name__ == "__main__":
    ships = getzkbships()

    main()

    # Sleep for 1 hour before ending and triggering another run via supervisor
    print("[Completed Run:Sleeping for 1 Hour]")
    sys.stdout.flush()
    sleep(3600)
