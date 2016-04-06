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


#
# Input     regionIDs, typeIDs
# Get       CREST market history
# Output    database insert
#
def market_getcrestdata(regionID, typeID):
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
        log = "[typeID:" + str(typeID) + "][regionID:" + str(regionID) + "][insert: " + str(count) + "]"
        insertlog("consumer_markethistory.py", 0, log, timemark)
        return 0
