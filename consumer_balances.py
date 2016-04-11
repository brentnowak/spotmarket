#-----------------------------------------------------------------------------
# consumer_balances.py
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

from _utility import *
from _balances import *
import evelink.char
import evelink.api

def main():
    service = "consumer_balances.py"

    # Get characters with walletEnabled = 1
    characters = json.loads(getcharacters())  # TODO rewrite function to return results specific to each consumer

    for character in characters:
        characterID = character['characterID']
        keyID = character['keyID']
        vCode = character['vCode']

        api_key = (keyID, vCode)
        eveapi = evelink.api.API(base_url='api.eveonline.com', api_key=api_key)
        charapi = evelink.char.Char(characterID, eveapi)
        charresponse = charapi.wallet_balance()
        charresponse = charresponse[0]

        balance = charresponse

        timestamp = arrow.now()
        timestamp = timestamp.format('YYYY-MM-DD HH:mm:ss')

        insertwalletbalances(characterID, balance, timestamp)

if __name__ == "__main__":
    main()
