#############################
# Dependencies
#############################

import psycopg2
import ConfigParser
import pandas as pd

#############################
# Database
#############################

config = ConfigParser.ConfigParser()
config.read(["config.ini"])
password = config.get("DATABASE", "password")
user = config.get("DATABASE", "user")
host = config.get("DATABASE", "host")
port = config.get("DATABASE", "port")
database_spotmarket = config.get("DATABASE", "database")

# Connection String
conn_string = "host=%s dbname=%s user=%s password=%s" % (host, database_spotmarket, user, password)


# Console
# Display wider outputs when debugging
desired_width = 320
pd.set_option('display.width', desired_width)


#############################
# Functions
#############################


#
# Input     regionID
# Output    regionName
#
def regionname(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT "mapRegions"."regionName" FROM public."mapRegions" WHERE "mapRegions"."regionID" = %s'
    data = (regionID, )
    cursor.execute(sql, data)
    result = cursor.fetchall()
    cursor.close()
    return result


#
# Input     regionID
# Output    dataframe of SUM_factionKills grouped by timestamp
#
def getnpckills_byregion(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = """SELECT
      SUM(mapkills."factionKills") as SUM_factionKills, timestamp
    FROM
      data.mapkills,
      public."mapSolarSystems"
    WHERE
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID"
        AND public."mapSolarSystems"."regionID" = %s
    GROUP BY mapkills."timestamp"
    ORDER BY timestamp DESC
    """
    data = (regionID, )
    cursor.execute(sql, data)
    df = pd.DataFrame(cursor.fetchall(),columns=['SUM_factionKills','timestamp'])
    cursor.close()
    return df

#
# Input         mapapi_data
# Output        Database insert
#
def insertmap(mapapi_data, maptimestamp):
    count_insert = 0
    for key,value in mapapi_data.iteritems():
        id = value['id']
        ship = value['ship']
        faction = value['faction']
        pod = value['pod']
        mapinsertrecord(maptimestamp, id, ship, faction, pod)
        count_insert += 1
    return count_insert

#
# Insert mapapi_data record
#
def mapinsertrecord(timestamp, id, ship, faction, pod):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'INSERT INTO data."mapkills" (timestamp, "solarSystemID", "shipKills", "factionKills", "podKills") VALUES (%s, %s, %s, %s, %s)'
    data = (timestamp, id, ship, faction, pod, )
    cursor.execute(sql, data)
    conn.commit()
    return 0

#
# Input         jumpsapi_data
# Output        Database insert
#
def insertjumps(jumps_data, jumpstimestamp):
    count_insert = 0
    for key,value in jumps_data.iteritems():
        id = key
        jumps = value
        jumpsinsertrecord(jumpstimestamp, id, jumps)
        count_insert += 1
    return count_insert

#
# Insert jumpsapi_data record
#
def jumpsinsertrecord(timestamp, id, jumps):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'INSERT INTO data."mapjumps" (timestamp, "solarSystemID", "shipJumps") VALUES (%s, %s, %s)'
    data = (timestamp, id, jumps, )
    cursor.execute(sql, data)
    conn.commit()
    return 0

