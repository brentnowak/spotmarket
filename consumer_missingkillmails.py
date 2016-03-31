#-----------------------------------------------------------------------------
# consumer_missingkillmails.py
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

from _utility import *
from requests.exceptions import ConnectionError, ChunkedEncodingError
import requests.packages.urllib3
from _consumer_kills import *

requests.packages.urllib3.disable_warnings()
#  Suppress InsecurePlatformWarning messages

service = "consumer_missingkillmails.py"

total = gettotalkmemptyvalues()

while getkmemptyvalue() != None:
    try:
        results = getkmemptyvalue()

        url = 'https://zkillboard.com/api/killID/' + str(results['killID']) + "/"
        headers = {'user-agent': 'github.com/brentnowak/spotmarket'}

        try:
            r = requests.get(url, headers=headers)
        except (ConnectionError, ChunkedEncodingError) as e:
            print(e)
        else:
            for kill in json.loads(r.text):
                if kill['killID'] == results['killID']:  # Check to confirm we have the correct Killmail
                    setkmtotalvalue(results['killID'], kill['zkb']['totalValue'])
                    print("[total:" + str(total) + "][killID:" + str(results['killID']) + "][totalValue:" + str(kill['zkb']['totalValue']) + "]")
                    total -= 1
    except Exception as e:
        print(e)

print("[km][all killmail values populated]")

