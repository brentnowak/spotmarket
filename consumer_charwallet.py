#-----------------------------------------------------------------------------
# consumer_charwallet.py
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

from _consumer_charwallet import *
from time import sleep
import sys
import evelink.char
import evelink.api
import evelink.parsing.wallet_transactions

def main():
    service = "consumer_charwallet.py"

    # Get characters with walletEnabled = 1
    characters = json.loads(getcharacters())

    for character in characters:
        characterName = character['characterName']
        characterID = character['characterID']
        walletID = character['walletID']
        keyID = character['keyID']
        vCode = character['vCode']

        api_key = (keyID, vCode)
        eveapi = evelink.api.API(base_url='api.eveonline.com', api_key=api_key)
        charapi = evelink.char.Char(characterID, eveapi)
        charresponse = charapi.wallet_transactions()
        charresponse = charresponse[0]

        insertcount = 0
        for row in charresponse:
            transactionDateTime = row['timestamp']
            transactionDateTime = arrow.get(transactionDateTime)
            transactionDateTime = transactionDateTime.format('YYYY-MM-DD HH:mm:ss')
            transactionID = row['id']
            quantity = row['quantity']
            typeName = row['type']['name']
            typeID = row['type']['id']
            price = row['price']
            clientID = row['client']['id']
            clientName = row['client']['name']
            walletID = walletID
            stationID = row['station']['id']
            #stationName = row['station']['name'] Not used
            transactionType = row['action']
            transactionFor = row['for']
            journalTransactionID = row['journal_id']
            personal = 0 # TODO allow user to true/false switch items for personal use
            profit = 0 # TODO profit calculations based on a first in/first out movement if items in a inventory table
            insertcount += insertwallettransaction(transactionDateTime, transactionID, quantity, typeName, typeID, price, clientID,
                                    clientName, characterID, stationID, transactionType, personal, profit, transactionFor, journalTransactionID)

        detail = "[character:" + str(characterName) + "][insert:" + str(insertcount) + "]"
        timestamp = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss')
        insertlog(service, 0, detail, timestamp)

if __name__ == "__main__":
    main()
    # Sleep for 1 hour + extra before ending and triggering another run via supervisor
    print("[Completed Run:Sleeping for 1 Hour]")
    sys.stdout.flush()
    sleep(3900)
