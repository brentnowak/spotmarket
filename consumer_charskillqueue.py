#-----------------------------------------------------------------------------
# consumer_charskillqueue.py
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

from _character import *
from time import sleep
import sys
import evelink.char
import evelink.api
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()
#  Suppress InsecurePlatformWarning messages

def main():
    service = "consumer_charskillqueue.py"

    characters = json.loads(getcharacters())

    # Empty table
    character_trunkskillqueue()

    for character in characters:
        characterID = character['characterID']
        keyID = character['keyID']
        vCode = character['vCode']

        api_key = (keyID, vCode)
        eveapi = evelink.api.API(base_url='api.eveonline.com', api_key=api_key)
        charapi = evelink.char.Char(characterID, eveapi)
        charresponse = charapi.skill_queue()
        charresponse = charresponse[0]

        for row in charresponse:
            end_ts = row['end_ts']
            level = row['level']
            type_id = row['type_id']
            start_ts = row['start_ts']
            end_sp = row['end_sp']
            start_sp = row['start_sp']
            position = row['position']

            end_ts = arrow.get(end_ts)
            end_ts = end_ts.format('YYYY-MM-DD HH:mm:ss')
            start_ts = arrow.get(start_ts)
            start_ts = start_ts.format('YYYY-MM-DD HH:mm:ss')

            character_insertskillqueue(characterID, end_ts, level, type_id, start_ts, end_sp, start_sp, position)

if __name__ == "__main__":
    main()
    # Sleep for 1 hour + extra before ending and triggering another run via supervisor
    print("[Completed Run:Sleeping for 1 Hour]")
    sys.stdout.flush()
    sleep(3900)
