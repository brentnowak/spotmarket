# Source    http://rischwa.net/coalitions/
# Input     http://rischwa.net/api/coalitions/current
# Output    meta."collation"

import sys
import requests
from _meta import *
from time import sleep


def main():
    r = requests.get('http://rischwa.net/api/coalitions/current')
    result = r.json()
    result = result['coalitions']

    for row in result:
        coalitionID = row['_id']
        coalitionName = row['name']
        coalition_insertcollation(coalitionID, coalitionName)
        for alliance in row['alliances']:
            #ticker = alliance['shortName']
            #name = alliance['name']
            allianceID = alliance['id']
            collation_updatecoalition(coalitionID, allianceID)


if __name__ == "__main__":
    main()

    # Sleep before ending and triggering another run via supervisor
    print("[Completed Run:Sleeping for 12 Hours]")
    sys.stdout.flush()
    sleep(3900)
