#-----------------------------------------------------------------------------
# process_validatejump.py
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

from _utility import *
import sys


def mapjump_allsolarsystems():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''
    SELECT DISTINCT("solarSystemID")
      FROM map.jump
    '''
    cursor.execute(sql, )
    results = cursor.fetchall()
    return results


def mapjump_alltimestamps(solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''
    SELECT timestamp::text
      FROM map.jump
    WHERE "solarSystemID" = %s
    '''
    data = (solarSystemID, )
    cursor.execute(sql, data, )
    results = cursor.fetchall()
    return results    


def mapjump_duplicatecheck(solarSystemID, timestamp):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''
    SELECT "systemjumpID", "timestamp", "shipJumps", "solarSystemID"
      FROM map.jump
    WHERE "solarSystemID" = %s AND
    "timestamp"::text LIKE %s
    '''
    data = (solarSystemID, timestamp, )
    cursor.execute(sql, data, )
    results = cursor.fetchall()
    return results


def mapjump_deleteduplicate(systemjumpID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''
    DELETE
      FROM map.jump
    WHERE "systemjumpID" = %s
    '''
    data = (systemjumpID, )
    cursor.execute(sql, data, )
    conn.commit()
    return 0


def main():
    solarSystems = mapjump_allsolarsystems()
    #solarSystems = [(30002187,)]  # Testing 1 solarSystemID
    currentSolarSystems = float(1)
    totalSolarSystems = float(len(solarSystems))
    for solarSystem in solarSystems:
        percentSolarSystems = "{0:.2f}".format(currentSolarSystems / totalSolarSystems * 100)
        timestamps = mapjump_alltimestamps(solarSystem)
        currentTimestamps = float(1)
        totalTimestamps = float(len(timestamps))
        for timestamp in timestamps:
            percentTimestamps = "{0:.2f}".format(currentTimestamps/totalTimestamps*100)
            timestamp = timestamp[0]
            timestamp = timestamp[:-2]
            timestamp = str(timestamp) + "%"
            results = mapjump_duplicatecheck(solarSystem[0], timestamp)
            if len(results) == 2:  # If we have duplicate
                print("[" + str(percentSolarSystems) + "%][" + str(percentTimestamps) + "%][" + str(solarSystem[0]) + "][Duplicate][" + str(timestamp) + "]")
                sys.stdout.flush()
                if results[0]['shipJumps'] == results[1]['shipJumps']:  # We have a duplicate
                    mapjump_deleteduplicate(results[1]['systemjumpID'])
            else:
                None
                #print("[" + str(percentTimestamps) + "%][" + str(solarSystem[0]) + "][No][" + str(timestamp) + "]")
            currentTimestamps += 1
        currentSolarSystems += 1

if __name__ == "__main__":
    main()
