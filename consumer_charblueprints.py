#-----------------------------------------------------------------------------
# consumer_charblueprints.py
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

from _utility import *
from _consumer_charblueprints import *
import evelink.char
import evelink.api

def main():
    service = "consumer_charblueprints.py"

    # Get characters with walletEnabled = 1
    characters = json.loads(getcharacters())  # TODO rewrite function to return results specific to each consumer

    # Empty table
    trunkcharblueprints()

    for character in characters:
        characterID = character['characterID']
        keyID = character['keyID']
        vCode = character['vCode']

        api_key = (keyID, vCode)
        eveapi = evelink.api.API(base_url='api.eveonline.com', api_key=api_key)
        charapi = evelink.char.Char(characterID, eveapi)
        charresponse = charapi.blueprints()
        charresponse = charresponse[0]

        for key, value in charresponse.iteritems():
            itemID = key
            locationID = value['location_id']
            typeID = value['type_id']
            quantity = value['quantity']
            flagID = value['location_flag']
            timeEfficiency = value['time_efficiency']
            materialEfficiency = value['material_efficiency']
            runs = value['runs']

            insertblueprintsitems(characterID, itemID, locationID, typeID, quantity, flagID, timeEfficiency, materialEfficiency, runs)

if __name__ == "__main__":
    main()
