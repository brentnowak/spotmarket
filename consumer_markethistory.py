#-----------------------------------------------------------------------------
# consumer_markethistory.py -
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------
#
# Input: List of typeIDs from 'data.marketitems' table that have 'enabled' set to 1.
# Output: Populate 'data.markethistory' table. Prices are currenlty only set for the Forge.
#-----------------------------------------------------------------------------

from _utility import *

def getmarketrecords(): # TODO Move function to _utility.py
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

def main():
    # TODO Allow user to select regions for price data
    # The Forge
    regionIDs = ['10000002']

    typeIDs = getmarketrecords()
    for typeID in typeIDs:
        print(typeID[0])
        getmarkethistory(10000002, typeID[0])


if __name__ == "__main__":
    main()
