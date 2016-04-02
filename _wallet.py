#############################
# Wallet
#############################

from _utility import *

def getwallet_typeid(typeID, transactionType):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      to_char(charwallet."transactionDateTime", 'YYYY-MM-dd HH:mm:ss') AS timestamp,
      "invTypes"."typeName",
      charwallet.quantity,
      charwallet.price,
      charwallet.quantity * charwallet.price as totalprice,
      charwallet.profit,
      "mapDenormalize"."itemName" as stationName,
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems".security,
      "mapRegions"."regionName"
    FROM
      data.charwallet,
      public."invTypes",
      public."mapSolarSystems",
      public."mapRegions",
      public."mapDenormalize"
    WHERE
      charwallet."typeID" = "invTypes"."typeID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapDenormalize"."itemID" = charwallet."stationID" AND
      "mapDenormalize"."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      charwallet."typeID" = %s AND
      charwallet."transactionType" = %s AND
      personal = 0
    ORDER BY
      charwallet."transactionDateTime" DESC'''
    data = (typeID, transactionType, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall())
    cursor.close()
    return df.reset_index().to_json(orient='records', date_format='iso')


def getprofitpersolarsystem(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      SUM(charwallet.profit) as sumProfit,
      SUM(charwallet.quantity) as sumQuantity,
      SUM(charwallet.profit) / SUM(charwallet.quantity) as averageProfit,
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName"
    FROM
      data.charwallet,
      public."mapDenormalize",
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
      charwallet."stationID" = "mapDenormalize"."itemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapDenormalize"."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      charwallet."typeID" = 12038
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


def getregionalstats(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      DISTINCT ON ("mapRegions"."regionName") "mapRegions"."regionName",
      markethistory."avgPrice",
      markethistory.volume
    FROM
      data.markethistory,
      public."mapRegions"
    WHERE
      "mapRegions"."regionID" = markethistory."regionID" AND
      "typeID" = %s
    GROUP BY
      "mapRegions"."regionName",
      markethistory."avgPrice",
      markethistory.volume,
      "mapRegions"."regionName",
      markethistory."timestamp"
    ORDER BY
     "mapRegions"."regionName" DESC
    '''
    data = (typeID,)
    cursor.execute(sql, data, )
    results = cursor.fetchall()
    cursor.close()
    return results
