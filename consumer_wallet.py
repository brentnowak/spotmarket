#-----------------------------------------------------------------------------
# consumer_wallet.py - EVE Online XML API consumer
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

from _utility import *
import evelink.char
import evelink.api
import evelink.parsing.wallet_transactions

def main():
    service = "consumer_wallet.py"

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

        for row in charresponse:
            transactionDateTime = row['timestamp']
            transactionID = row['journal_id']
            quantity = row['quantity']
            typeName = row['type']['name']
            typeID = row['type']['id']
            price = row['price']
            clientID = row['client']['id']
            clientName = row['client']['name']
            walletID = walletID
            stationID = row['station']['id']
            stationName = row['station']['name']
            transactionType = row['action']
            personal = 0
            profit = 0
            insertcount = insertwallettransaction(transactionDateTime, transactionID, quantity, typeName, typeID, price, clientID, clientName, walletID, stationID, stationName, transactionType, personal, profit)
            detail = "[wallet " + str(walletID) + "] insert " + str(insertcount)
            timestamp = arrow.get() # Get arrow object
            timestamp = timestamp.timestamp # Get timestamp of arrow object
            insertlog_timestamp(service, 0, detail, timestamp)

if __name__ == "__main__":
    main()