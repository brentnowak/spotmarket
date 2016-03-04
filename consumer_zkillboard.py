from _utility import *

#############################
#
# Work in progress
#
#############################

response = '{"solarSystem": {"id_str": "30001982", "href": "https://public-crest.eveonline.com/solarsystems/30001982/", "id": 30001982, "name": "G95-VZ"}, "killID": 52250409, "killTime": "2016.02.25 17:38:02", "attackers": [{"alliance": {"id_str": "1354830081", "href": "https://public-crest.eveonline.com/alliances/1354830081/", "id": 1354830081, "name": "Goonswarm Federation", "icon": {"href": "http://imageserver.eveonline.com/Alliance/1354830081_128.png"}}, "shipType": {"id_str": "17713", "href": "https://public-crest.eveonline.com/types/17713/", "id": 17713, "name": "Stabber Fleet Issue", "icon": {"href": "http://imageserver.eveonline.com/Type/17713_128.png"}}, "corporation": {"id_str": "2052404106", "href": "https://public-crest.eveonline.com/corporations/2052404106/", "id": 2052404106, "name": "Valar Morghulis.", "icon": {"href": "http://imageserver.eveonline.com/Corporation/2052404106_128.png"}}, "character": {"id_str": "90170963", "href": "https://public-crest.eveonline.com/characters/90170963/", "id": 90170963, "name": "LordShazbot", "icon": {"href": "http://imageserver.eveonline.com/Character/90170963_128.jpg"}}, "damageDone_str": "79895", "weaponType": {"id_str": "2488", "href": "https://public-crest.eveonline.com/types/2488/", "id": 2488, "name": "Warrior II", "icon": {"href": "http://imageserver.eveonline.com/Type/2488_128.png"}}, "finalBlow": true, "securityStatus": -3.3, "damageDone": 79895}], "attackerCount": 1, "victim": {"damageTaken": 79895, "items": [{"singleton": 0, "itemType": {"id_str": "16641", "href": "https://public-crest.eveonline.com/types/16641/", "id": 16641, "name": "Chromium", "icon": {"href": "http://imageserver.eveonline.com/Type/16641_128.png"}}, "quantityDestroyed_str": "324", "flag": 5, "flag_str": "5", "singleton_str": "0", "quantityDestroyed": 324}], "damageTaken_str": "79895", "character": {"id_str": "1072804170", "href": "https://public-crest.eveonline.com/characters/1072804170/", "id": 1072804170, "name": "StFlyer", "icon": {"href": "http://imageserver.eveonline.com/Character/1072804170_128.jpg"}}, "shipType": {"id_str": "33477", "href": "https://public-crest.eveonline.com/types/33477/", "id": 33477, "name": "Small Mobile Siphon Unit", "icon": {"href": "http://imageserver.eveonline.com/Type/33477_128.png"}}, "corporation": {"id_str": "98322687", "href": "https://public-crest.eveonline.com/corporations/98322687/", "id": 98322687, "name": "RESET.", "icon": {"href": "http://imageserver.eveonline.com/Corporation/98322687_128.png"}}, "position": {"y": 867902945.0184605, "x": 1743710307568.5635, "z": -5246218890326.316}}, "killID_str": "52250409", "attackerCount_str": "1", "war": {"href": "https://public-crest.eveonline.com/wars/0/", "id": 0, "id_str": "0"}}'
response = json.loads(response)
solarSystemID = response['solarSystem']['id']
killID = response['killID']
killTime = response['killTime']
typeID = response['victim']['items'][0]['itemType']['id']
typeName = response['victim']['items'][0]['itemType']['name']
#shipType = ['victim']['shipType']
x = response['victim']['position']['x']
y = response['victim']['position']['y']
z = response['victim']['position']['z']

print(solarSystemID)
print(killID)
print(killTime)
#print(shipType)
print(typeID)
print(typeName)
print(x, y, z)


