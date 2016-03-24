import psutil
from _utility import *


def timeutc():
    return arrow.utcnow().format('YYYY-MM-DD HH:mm:ss')


def countdatakillmails():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
        COUNT(*)
        FROM data.killmails'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]


def countdatawallet():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
        COUNT(*)
        FROM data.wallet'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]


def countdatamarkethistory():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
        COUNT(*)
        FROM data.markethistory'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]


def countdatamoonminerals():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
        COUNT(DISTINCT "moonID")
        FROM data.moonminerals'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]


def countdatamoonverify():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
        COUNT(DISTINCT "moonID")
        FROM data.moonverify'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]


def countlatestjitajump():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapjumps."shipJumps"
    FROM
      public."mapSolarSystems",
      data.mapjumps
    WHERE
      mapjumps."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."solarSystemID" = 30000142
    LIMIT 1'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]


def latestjumpdatatime():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapjumps."timestamp"
    FROM
      public."mapSolarSystems",
      data.mapjumps
    WHERE
      mapjumps."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."solarSystemID" = 30000142
    LIMIT 1'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]


def latestsovdatatime():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapsov."timestamp"
    FROM
      data.mapsov
    ORDER BY timestamp DESC
    LIMIT 1'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]


def psutil_getmemory():
    return psutil.virtual_memory().percent


def psutil_crestconnections():  # TODO change hardcoded IP to IP with DNS lookup
    count = 0
    results = psutil.net_connections(kind='inet4')
    for row in results:
        connection = row[4]
        if len(connection) > 0:
            if connection[0] == "87.237.34.206":  # CREST Public IP
                count += 1
    return count


def psutil_zkillboardconnections():  # TODO change hardcoded IP to IP with DNS lookup
    count = 0
    results = psutil.net_connections(kind='inet4')
    for row in results:
        connection = row[4]
        if len(connection) > 0:
            if connection[0] == "104.24.30.39":  # zKillboard Public IP
                count += 1
    return count


def getlatestprice(typeID, regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      markethistory."avgPrice"
    FROM
      data.markethistory
    WHERE markethistory."typeID" = %s AND
    markethistory."regionID" = %s
    ORDER BY timestamp DESC
    LIMIT 1'''
    data = (typeID, regionID, )
    cursor.execute(sql, data)
    result = cursor.fetchone()
    return result[0]


def getpricepercentchange(typeID, regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      (1 - markethistory."avgPrice" / LAG(markethistory."avgPrice") OVER (ORDER BY markethistory."timestamp")) * 100 AS pct_change
    FROM
      data.markethistory
    WHERE
      markethistory."typeID" = 29668 AND
      markethistory."regionID" = 10000002
    ORDER BY timestamp DESC
    LIMIT 1'''
    data = (typeID, regionID, )
    cursor.execute(sql, data)
    result = cursor.fetchone()
    return result[0]


def getwallettransactions(limit):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      wallet."typeName",
      wallet.quantity,
      wallet."typeID",
      wallet.price,
      wallet.profit,
      wallet."transactionDateTime"
    FROM
      data.wallet
    ORDER BY
     wallet."transactionDateTime" DESC
    LIMIT %s'''
    data = (limit, )
    cursor.execute(sql, data)
    results = cursor.fetchall()  # TODO return dictionary rather than list
    return results
