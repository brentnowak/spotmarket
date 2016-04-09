#############################
# Wallet
#############################

from _utility import *

def getwallet_typeid(typeID, transactionType):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      to_char(wallet."transactionDateTime", 'YYYY-MM-dd HH:mm:ss') AS timestamp,
      "invTypes"."typeName",
      wallet.quantity,
      wallet.price,
      wallet.quantity * wallet.price as totalprice,
      wallet.profit,
      "mapDenormalize"."itemName" as stationName,
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems".security,
      "mapRegions"."regionName"
    FROM
      "character".wallet,
      public."invTypes",
      public."mapSolarSystems",
      public."mapRegions",
      public."mapDenormalize"
    WHERE
      wallet."typeID" = "invTypes"."typeID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapDenormalize"."itemID" = wallet."stationID" AND
      "mapDenormalize"."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      wallet."typeID" = %s AND
      wallet."transactionType" = %s AND
      personal = 0
    ORDER BY
      wallet."transactionDateTime" DESC'''
    data = (typeID, transactionType, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall())
    cursor.close()
    return df.reset_index().to_json(orient='records', date_format='iso')


def getprofitpersolarsystem(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      SUM(wallet.profit) as sumProfit,
      SUM(wallet.quantity) as sumQuantity,
      SUM(wallet.profit) / SUM(wallet.quantity) as averageProfit,
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName"
    FROM
      "character".wallet,
      public."mapDenormalize",
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
      wallet."stationID" = "mapDenormalize"."itemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapDenormalize"."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      wallet."typeID" = %s
    GROUP BY
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName"
    ORDER BY
     averageProfit DESC'''
    data = (typeID, )
    cursor.execute(sql, data, )
    results = cursor.fetchall()
    cursor.close()
    return results


def getallwallettransactions():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      to_char(wallet."transactionDateTime", 'YYYY-MM-dd HH:mm:ss') AS timestamp,
      quantity,
      "typeName",
      wallet."typeID",
      wallet."typeID" as "iconID",
      price,
      "stationID",
      "transactionType",
      personal,
      profit,
      "mapDenormalize"."itemName" as "stationName",
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName"
    FROM "character".wallet,
      public."mapDenormalize",
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
      wallet."stationID" = "mapDenormalize"."itemID" AND
      "mapSolarSystems"."solarSystemID" = "mapDenormalize"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID"
    ORDER BY
     wallet."transactionDateTime" DESC'''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results
