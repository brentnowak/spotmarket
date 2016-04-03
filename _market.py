from _utility import *

def getmarkettypeids():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      marketitems."typeID"
    FROM
      data.marketitems
    WHERE marketitems.enabled = 1
    '''
    cursor.execute(sql, )
    results = cursor.fetchall()
    if results == None:  # Error checking if table is empty
            return 0
    else:
        return results


def getmarketregionids():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      marketregions."regionID"
    FROM
      data.marketregions
    WHERE marketregions.enabled = 1
    '''
    cursor.execute(sql, )
    results = cursor.fetchall()
    if results == None:  # Error checking if table is empty
        return 0
    else:
        return results


#
# Input     regionIDs, typeIDs
# Output    database insert
#
def insertmarkethistory(regionID, typeID):
    eve = pycrest.EVE()
    start_time = time.time()
    url = "https://public-crest.eveonline.com/market/" + str(regionID) + "/types/" + str(typeID) + "/history/"
    try:
        history = eve.get(url)
    except Exception: # TODO Implement better exception handling for CREST API
        timemark = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss')
        log = "[typeID:" + str(typeID) + "][regionID:" + str(regionID) + "] Exception"
        insertlog("consumer_markethistory.py", 5, log, timemark)
        return 0
    else:
        count = insertmarketrecord(regionID, typeID, history)
        timemark = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss')
        log = "[typeID:" + str(typeID) + "][regionID:" + str(regionID) + "] insert: " + str(count) + " @ " + str(round(count/(time.time() - start_time), 2)) + " rec/sec"
        insertlog("consumer_markethistory.py", 0, log, timemark)
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        sql = '''UPDATE
        data.marketitems
        SET "importResult" = 1
        WHERE marketitems."typeID" = %s
        '''
        data = (typeID, )
        cursor.execute(sql, data, )
        conn.close()
        return 0
