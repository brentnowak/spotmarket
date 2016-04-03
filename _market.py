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
