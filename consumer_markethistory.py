#-----------------------------------------------------------------------------
# consumer_markethistory.py - EVE Online CREST API consumer
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

from _utility import *

def getlatestmarketrecord():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      marketitems."typeID"
    FROM
      data.marketitems
    WHERE marketitems."importResult" < 1
    LIMIT 1
    '''
    cursor.execute(sql, )
    result = cursor.fetchone()
    if result == None:  # Error checking if table is empty
            return 0
    else:
        return result[0]

def main():

    # The Forge
    regionIDs = ['10000002']
    #1041	Advanced Commodities
    #getmarkethistory(regionIDs)

    typeID = getlatestmarketrecord()
    print(typeID)
    getmarkethistory(10000002, typeID)


if __name__ == "__main__":
    main()