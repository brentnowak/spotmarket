from _utility import *
import evelink.char
import evelink.api
import evelink.parsing.wallet_transactions

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
        insertlog("")
        print(insertcount)
