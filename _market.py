import sys
from _utility import *

def market_typeids():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      tracking."typeID"
    FROM
      market.tracking
    WHERE tracking.enabled = 1
    ORDER BY tracking."typeID" ASC
    '''
    cursor.execute(sql, )
    results = cursor.fetchall()
    if results == None:
            return 0
    else:
        return results


def market_regionids():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      region."regionID"
    FROM
      market.region
    WHERE region.enabled = 1 AND
    region."importResult" = 0
    ORDER BY rank ASC
    '''
    cursor.execute(sql, )
    results = cursor.fetchall()
    if results == None:
        return 0
    else:
        return results


def market_setimportresult(regionID, importResult):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''UPDATE market.region
            SET "importResult" = %s
            WHERE region."regionID" = %s'''
    data = (importResult, regionID, )
    cursor.execute(sql, data, )
    conn.commit()
    conn.close()
    return 0


def market_getregionalprices(typeID, regionIDs):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      "mapRegions"."regionName",
      history."avgPrice",
      to_char(history."timestamp", 'YYYY-MM-dd') AS timestamp
    FROM
      market.history,
      public."mapRegions",
      public."invTypes"
    WHERE
      history."regionID" = "mapRegions"."regionID" AND
      "invTypes"."typeID" = history."typeID" AND
      "invTypes"."typeID" = %s AND
      history."regionID" IN %s AND
      history."timestamp" > '2016-01-01'
    GROUP BY
      history."regionID",
      "mapRegions"."regionName",
      history."avgPrice",
      history.volume,
      history."timestamp"
    ORDER BY
      history."timestamp" DESC'''
    data = (typeID, regionIDs, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall())
    cursor.close()
    df = pd.pivot_table(df, index='timestamp', columns='regionName', values='avgPrice')
    df = df.fillna(method='pad')
    return df.reset_index().to_json(orient='records', date_format='iso')
    #return df


def getmarkethistory_typeID(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
       history."typeID",
       "invTypes"."typeName",
       history."regionID",
       to_char(history."timestamp", 'YYYY-MM-dd') AS timestamp,
       history.volume,
       history."orderCount",
       history."lowPrice",
       history."highPrice",
       history."avgPrice"
    FROM
       public."invTypes",
       market.history
     WHERE history."typeID" = "invTypes"."typeID" AND
       history."typeID" = %s
     ORDER BY history."timestamp" DESC'''
    data = (typeID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall())
    df = df.fillna(method='pad')
    return df.reset_index().to_json(orient='records', date_format='iso')


def getmarkethistory_avgprice(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      to_char(history."timestamp", 'YYYY-MM-dd') AS timestamp,
      history."avgPrice" AS "The Forge"
    FROM
      market.history
     WHERE history."typeID" = %s AND
       history."regionID" = 10000002 AND
       history."timestamp" > '2016-01-01'
     ORDER BY history."timestamp" DESC'''
    data = (typeID,)
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall())
    df = df.set_index(['timestamp'])
    df = df.fillna(method='pad')
    return df.reset_index().to_json(orient='records', date_format='iso')


def getregionalstats(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      DISTINCT ON ("mapRegions"."regionName") "mapRegions"."regionName",
      history."avgPrice",
      history.volume
    FROM
      market.history,
      public."mapRegions"
    WHERE
      "mapRegions"."regionID" = history."regionID" AND
      history."regionID" IN %s AND
      "typeID" = %s
    GROUP BY
      "mapRegions"."regionName",
      history."avgPrice",
      history.volume,
      "mapRegions"."regionName",
      history."timestamp"
    ORDER BY
     "mapRegions"."regionName" DESC
    '''
    data = (topOfBook, typeID,)
    cursor.execute(sql, data, )
    results = cursor.fetchall()
    cursor.close()
    return results


#
# Input     regionIDs, typeIDs
# Get       CREST market history
# Output    database insert
#
def market_getcrestdata(regionID, typeID):
    latestDate = market_getlatestdate(typeID, regionID)
    eve = pycrest.EVE()
    url = "https://public-crest.eveonline.com/market/" + str(regionID) + "/types/" + str(typeID) + "/history/"
    try:
        crestData = eve.get(url)
    except Exception as e:
        timemark = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss')
        log = "[typeID:" + str(typeID) + "][regionID:" + str(regionID) + "][" + str(e) + "]"
        insertlog("consumer_markethistory.py", 5, log, timemark)
        return 0
    else:
        count = 0
        for row in crestData['items']:
            volume = row['volume']
            orderCount = row['orderCount']
            lowPrice = row['lowPrice']
            highPrice = row['highPrice']
            avgPrice = row['avgPrice']
            timestamp = row['date']
            print(typeID)
            print(type(latestDate))
            print(type(timestamp))
            if timestamp > latestDate:  # Only import if CREST data is newer
                print("new data")
                try:
                    conn = psycopg2.connect(conn_string)
                    cursor = conn.cursor()
                    sql = '''INSERT INTO market.history ("typeID", "regionID", timestamp,
                     "volume", "orderCount", "lowPrice",
                      "highPrice", "avgPrice")
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
                    data = (typeID, regionID, timestamp, volume, orderCount, lowPrice, highPrice, avgPrice,)
                    cursor.execute(sql, data, )
                except psycopg2.IntegrityError:
                    conn.rollback()
                else:
                    conn.commit()
                    count += 1
        timemark = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss')
        print("[" + str(getregionName(regionID) + "][typeID:" + str(typeID) + "][" + str(gettypeName(typeID)) + "]"))
        sys.stdout.flush()
        log = "[typeID:" + str(typeID) + "][regionID:" + str(regionID) + "][insert: " + str(count) + "]"
        insertlog("consumer_markethistory.py", 0, log, timemark)
        return 1


def market_speculationpricechange():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''
    SELECT
      speculation."transactionID", speculation."typeID"
    FROM
      market.speculation
    '''
    cursor.execute(sql, )
    transactions = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame()
    for transaction in transactions:
        df = df.append(market_speculationpricechangeitem(transaction['typeID'], transaction['transactionID']))
    return df.reset_index().to_json(orient='records')


def market_speculationtotals():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''
    SELECT
      speculation."transactionID", speculation."typeID"
    FROM
      market.speculation
    '''
    cursor.execute(sql, )
    transactions = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame()
    for transaction in transactions:
        df = df.append(market_speculationpricechangeitem(transaction['typeID'], transaction['transactionID']))
    results = {}
    results['purchaseValue'] = df['purchaseValue'].sum()
    results['speculationValue'] = df['speculationValue'].sum()
    results['valueChange'] = df['valueChange'].sum()
    return results


def market_speculationpricechangeitem(typeID, transactionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      speculation."transactionID",
      speculation."typeID",
      speculation."typeID" as "iconID",
      "invTypes"."typeName",
      speculation.quantity,
      speculation.remaining,
      speculation.price as "purchasePrice",
      speculation.price * speculation.remaining as "purchaseValue",
      (SELECT
        history."avgPrice"
        FROM
        market.history
        WHERE "typeID" = %s AND
        "regionID" = 10000002
        ORDER BY "timestamp" DESC
        LIMIT 1) as "latestJitaPrice",
      (SELECT
        history."avgPrice"
        FROM
        market.history
        WHERE "typeID" = %s AND
        "regionID" = 10000002
        ORDER BY "timestamp" DESC
        LIMIT 1) * speculation.remaining as "speculationValue",
      (SELECT
        history."timestamp"
        FROM
        market.history
        WHERE "typeID" = %s AND
        "regionID" = 10000002
        ORDER BY "timestamp" DESC
        LIMIT 1) as "latestJitaTimestamp",
      ((SELECT
        history."avgPrice"
        FROM
        market.history
        WHERE "typeID" = %s AND
        "regionID" = 10000002
        ORDER BY "timestamp" DESC
        LIMIT 1) * speculation.remaining) - (speculation.price * speculation.remaining) as "valueChange"
    FROM
      market.speculation,
      public."invTypes"
    WHERE
      speculation."typeID" = "invTypes"."typeID" AND
      speculation."transactionID" = %s
    '''
    data = (typeID, typeID, typeID, typeID, transactionID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall())
    cursor.close()
    return df


def market_getlatestdate(typeID, regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      history."timestamp"
    FROM
      market.history
    WHERE
      history."typeID" = %s AND
      history."regionID" = %s
    ORDER BY history."timestamp" DESC
    LIMIT 1
    '''
    data = (typeID, regionID, )
    cursor.execute(sql, data, )
    result = cursor.fetchone()
    if result == None:
            return 0
    else:
        return result[0]
