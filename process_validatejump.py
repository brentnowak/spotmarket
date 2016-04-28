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


def mapjump_deleteduplicate(solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''
        DELETE FROM map.jump mj1 USING map.jump mj2
    WHERE (mj1."solarSystemID" = mj2."solarSystemID")
    AND mj1.timestamp >= mj2.timestamp - interval '1 sec'
    AND mj1.timestamp <= mj2.timestamp + interval '1 sec'
    AND mj1."solarSystemID" = mj2."solarSystemID"
    AND mj1."systemjumpID" != mj2."systemjumpID"
    AND mj1."systemjumpID" < mj2."systemjumpID"
    AND mj1."solarSystemID" = %s
    '''
    data = (solarSystemID, )
    cursor.execute(sql, data, )
    conn.commit()
    return 0


def main():
    solarSystems = mapjump_allsolarsystems()
    currentSolarSystems = float(1)
    totalSolarSystems = float(len(solarSystems))
    for solarSystem in solarSystems:
        mapjump_deleteduplicate(solarSystem)
        percentSolarSystems = "{0:.2f}".format(currentSolarSystems / totalSolarSystems * 100)
        print("[" + str(percentSolarSystems) + "%][" + str(getSolarSystemName(solarSystem[0])) + "]")
        sys.stdout.flush()
        currentSolarSystems += 1

if __name__ == "__main__":
    main()
