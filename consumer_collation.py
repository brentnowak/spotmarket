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
        collationName = row['name']
        collation_insertcollation(collationName)
        for alliance in row['alliances']:
            ticker = alliance['shortName']
            name = alliance['name']
            allianceID = alliance['id']
            print(str(name) + "," + str(allianceID))
        print("-------------------")



if __name__ == "__main__":
    main()

    # Sleep before ending and triggering another run via supervisor
    print("[Completed Run:Sleeping for 12 Hours]")
    sys.stdout.flush()
    sleep(3900)
