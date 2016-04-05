#-----------------------------------------------------------------------------
# consumer_validatekillmails.py
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

from _utility import *
from requests.exceptions import ConnectionError, ChunkedEncodingError
import requests.packages.urllib3
from _kills import *

requests.packages.urllib3.disable_warnings()
#  Suppress InsecurePlatformWarning messages

service = "consumer_validatekillmails.py"

totalEmptyValue = gettotalkmemptyvalues()
totalBadJSON = gettotalbadjson()

#
# Look for KMs with missing totalValues
#
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
                    print("[total:" + str(totalEmptyValue) + "][killID:" + str(results['killID']) + "][totalValue:" + str(kill['zkb']['totalValue']) + "]")
                    totalEmptyValue -= 1
    except Exception as e:
        print(e)

print("[validatekillmails][all killmail values populated]")

#
# Look for KMs with bad or missing CREST JSON
#
while getkmbadjson() != None:
    try:
        kill = getkmbadjson()
        print("[badJSON:" + str(totalBadJSON) + "][killiID:" + str(kill['killID']) + "]")
        crestURL = 'https://public-crest.eveonline.com/killmails/' + str(kill['killID']) + '/' + str(kill['killHash']) + '/'
        try:
            crestKill = requests.get(crestURL)
        except (ConnectionError, ChunkedEncodingError) as e:
            print(e)
        else:
            setkmjson(kill['killID'], crestKill.text)
            totalBadJSON -= 1
    except Exception as e:
        print(e)
print("[validatekillmails][all killmail json populated]")
