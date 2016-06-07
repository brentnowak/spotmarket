from _utility import *
from _map import *

def getcharacterblueprints():  # TODO add join to display regionName and solarSystemName
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      characters."characterName",
      "invTypes"."typeName",
      "invTypes"."typeID",
      blueprint.quantity,
      blueprint."timeEfficiency",
      blueprint."materialEfficiency",
      blueprint.runs
    FROM
      "character".blueprint,
      "character".characters,
      public."invTypes"
    WHERE
      blueprint."characterID" = characters."characterID" AND
      "invTypes"."typeID" = blueprint."typeID" AND
      characters."characterID" = blueprint."characterID"'''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    cursor.close()
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def getcharacterorders():  # TODO add join to display regionName and solarSystemName
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      characters."characterName",
      "invTypes"."typeName",
      orders."typeID" as "iconID",
      orders."volEntered",
      orders."volRemaining",
      orders.duration,
      orders."orderState",
      orders.price,
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName"
    FROM
      "character".orders,
      public."invTypes",
      public."mapDenormalize",
      public."mapSolarSystems",
      public."mapRegions",
      "character".characters
    WHERE
      orders."stationID" = "mapDenormalize"."itemID" AND
      orders."typeID" = "invTypes"."typeID" AND
      "mapDenormalize"."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      orders.bid = 'sell' AND
      characters."characterID" = orders."characterID"
      '''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    cursor.close()
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def market_inventoryadd(transactionID):  # Initial populate of item into market.inventory
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''INSERT INTO market.inventory(
            "transactionID", "typeID", quantity, remaining, price)
    SELECT "transactionID", "typeID", quantity, quantity AS remaining, price
    FROM "character".wallet
    WHERE wallet."transactionID" = %s
    ON CONFLICT DO NOTHING
    '''
    data = (transactionID, )
    cursor.execute(sql, data, )
    conn.commit()
    conn.close()
    return transactionID


def market_speculationadd(transactionID):  # Initial populate of item into market.speculation
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''INSERT INTO market.speculation(
            "transactionID", "typeID", quantity, remaining, price)
    SELECT "transactionID", "typeID", quantity, quantity AS remaining, price
    FROM "character".wallet
    WHERE wallet."transactionID" = %s
    ON CONFLICT DO NOTHING
    '''
    data = (transactionID, )
    cursor.execute(sql, data, )
    conn.commit()
    conn.close()
    return transactionID


def meta_conquerablestationslist():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      conquerablestation."solarSystemID",
      conquerablestation."stationID",
      conquerablestation.name AS stationName,
      alliance."allianceID",
      alliance.ticker,
      alliance.name AS allianceName,
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems".security,
      "mapRegions"."regionName"
    FROM
      meta.conquerablestation,
      meta.alliance,
      map.sov,
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
      conquerablestation."solarSystemID" = sov."solarSystemID" AND
      conquerablestation."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      sov."allianceID" = alliance."allianceID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID"'''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    cursor.close()
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def force_region(regionID):
    links = []
    nodes = map_solarsystems_region(regionID)
    idcount = 0
    value = 1
    # assign row ids
    for row in nodes:
        row['id'] = idcount
        idcount += 1
    for row in nodes:  # for every solarSystem
        connections = map_solarsystem_connections(row['solarSystemID'])
        source = row['id']

        for connection in connections:
            for row in nodes:
                if row['solarSystemID'] == connection['toSolarSystemID']:
                    target = row['id']
                    #print(nodes['solarSystemID'])
                    #print(connection['toSolarSystemID'])
                    #target = 1000
                    link = {'source': source, 'target': target, 'value': value}
                    links.append(link)

    result = {'nodes': nodes, 'links': links}
    return json.dumps(result)
