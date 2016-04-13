from _utility import *

def moon_regionsummary(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      COUNT(mineral."typeID") AS "countTypeID",
      "mapRegions"."regionName"
    FROM
      moon.mineral,
      public."invTypes",
      public."mapDenormalize",
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
      mineral."typeID" = "invTypes"."typeID" AND
      "mapDenormalize"."itemID" = mineral."moonID" AND
      "mapDenormalize"."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      mineral."typeID" = 16650
     GROUP BY  "mapRegions"."regionName"
     ORDER BY "countTypeID" DESC'''
    data = (typeID,)
    cursor.execute(sql, data, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    cursor.close()
    if len(results) < 1:  # Handle a empty table
        return "No Data"
    else:
        return results


def moon_regionsummarypie(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
    COUNT(mineral."moonID") as "sum_regionID",
      "mapRegions"."regionName" as "regionName"
    FROM
      moon.mineral,
      public."invTypes",
      public."mapDenormalize",
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
      mineral."typeID" = "invTypes"."typeID" AND
      "mapDenormalize"."itemID" = mineral."moonID" AND
      "mapDenormalize"."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      mineral."typeID" = 16650
     GROUP BY  "mapRegions"."regionName"
     ORDER BY "sum_regionID" DESC'''
    data = (typeID, )
    cursor.execute(sql, data, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    cursor.close()
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results
