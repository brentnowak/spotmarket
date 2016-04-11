import psutil
from _utility import *


def timeutc():
    return arrow.utcnow().format('YYYY-MM-DD HH:mm:ss')


def countuserstq():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT players
      FROM meta.tranquility
    ORDER BY timestamp DESC
    LIMIT 1'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    if result == None:
        return 0
    else:
        return result[0]


def statustq():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT status
      FROM meta.tranquility
    ORDER BY timestamp DESC
    LIMIT 1'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    if result == None:
        return "Error"
    if result[0] == True:
        return "Online"
    if result[0] == False:
        return "Offline"
    else:
        return "Error"


def countdatakillmails():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
        COUNT(*)
        FROM kill.mail'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    if result == None:
        return 0
    else:
        return result[0]


def countdatawallet():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
        COUNT(*)
        FROM "character".wallet'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    if result == None:
        return 0
    else:
        return result[0]


def countdatamarkethistory():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
        COUNT(*)
        FROM market.history'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    if result == None:
        return 0
    else:
        return result[0]


def countdatamoonminerals():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
        COUNT(DISTINCT "moonID")
        FROM moon.mineral'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    if result == None:
        return 0
    else:
        return result[0]


def countdatamoonverify():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
        COUNT(DISTINCT "moonID")
        FROM moon.killmail'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    if result == None:
        return 0
    else:
        return result[0]


def countlatestjitajump():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      jump."shipJumps"
    FROM
      public."mapSolarSystems",
      map.jump
    WHERE
      jump."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."solarSystemID" = 30000142
    LIMIT 1'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    if result == None:
        return 0
    else:
        return result[0]


def latestjumpdatatime():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      jump."timestamp"
    FROM
      public."mapSolarSystems",
      map.jump
    WHERE
      jump."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."solarSystemID" = 30000142
    LIMIT 1'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    if result == None:
        return 0
    else:
        return result[0]


def latestsovdatatime():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      sov."timestamp"
    FROM
      map.sov
    ORDER BY timestamp DESC
    LIMIT 1'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    if result == None:
        return 0
    else:
        return result[0]


def countsovchangelastday():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      COUNT(*)
    FROM
      map.sov
    WHERE sov."timestamp" >= NOW() - '1 day'::INTERVAL'''
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
      history."avgPrice"
    FROM
      market.history
    WHERE history."typeID" = %s AND
    history."regionID" = %s
    ORDER BY timestamp DESC
    LIMIT 1'''
    data = (typeID, regionID, )
    cursor.execute(sql, data)
    result = cursor.fetchone()
    if result == None:
        return 0
    else:
        return result[0]


def getpricepercentchange(typeID, regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      (1 - history."avgPrice" / LAG(history."avgPrice") OVER (ORDER BY history."timestamp")) * 100 AS pct_change
    FROM
      market.history
    WHERE
      history."typeID" = 29668 AND
      history."regionID" = 10000002
    ORDER BY timestamp DESC
    LIMIT 1'''
    data = (typeID, regionID, )
    cursor.execute(sql, data)
    result = cursor.fetchone()
    if result == None:
        return 0
    else:
        return result[0]


def getwallettransactions(limit):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      wallet."typeName",
      wallet.quantity,
      wallet."typeID",
      wallet.price,
      wallet.profit,
      wallet."transactionDateTime" as timestamp
    FROM
      "character".wallet
    ORDER BY
     wallet."transactionDateTime" DESC
    LIMIT %s'''
    data = (limit, )
    cursor.execute(sql, data, )
    results = cursor.fetchall()
    cursor.close()
    return results


def getwalletbalances():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''
    SELECT
    DISTINCT ON (characters."characterName") characters."characterName",
      characters."characterID",
      balance.balance,
      balance."timestamp"
    FROM
      "character".characters,
      "character".balance
    WHERE
      balance."characterID" = characters."characterID" AND
      characters."enableWallet" = 1
    GROUP BY  characters."characterName",
      balance.balance,
      characters."characterID",
      balance."timestamp"
    ORDER BY characters."characterName", balance."timestamp" DESC
    '''
    cursor.execute(sql, )
    results = cursor.fetchall()  # TODO return dictionary rather than list
    return results


def getwalletbalancestotal():
    total = 0
    results = getwalletbalances()
    for row in results:  #  TODO correct this to use dictionary rather than list
        total += int(row[2])
    return total


def getskillqueues():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      characters."characterID",
      characters."characterName",
      "invTypes"."typeName",
      skillqueue.level,
      skillqueue."endTime" - current_timestamp as timeLeft,
      (CAST(EXTRACT(EPOCH FROM current_timestamp) AS FLOAT) - CAST(EXTRACT(EPOCH FROM skillqueue."startTime") AS FLOAT)) / (CAST(EXTRACT(EPOCH FROM skillqueue."endTime") AS FLOAT) - CAST(EXTRACT(EPOCH FROM skillqueue."startTime") AS FLOAT)) * 100 AS progress
    FROM
      "character".characters,
      "character".skillqueue,
      public."invTypes"
    WHERE
      characters."characterID" = skillqueue."characterID" AND
      skillqueue."typeID" = "invTypes"."typeID" AND
      skillqueue."queuePosition" = 0 AND
      CAST(EXTRACT(EPOCH FROM skillqueue."endTime") AS INTEGER) != CAST(EXTRACT(EPOCH FROM skillqueue."startTime") AS INTEGER)'''
    cursor.execute(sql, )
    results = cursor.fetchall()  # TODO return dictionary rather than list
    return results


def databasecountmapkills():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT COUNT(*) FROM map.kills'
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def databasecountmapjumps():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT COUNT(*) FROM map.jumps'
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def databasecountmapsov():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT COUNT(*) FROM map.sov'
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def databasecountmarkethistory():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT COUNT(*) FROM market.history'
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results
