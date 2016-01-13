#-----------------------------------------------------------------------------
# consumer.py - EVE Online API consumer
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 1.0
# - Initial release
#-----------------------------------------------------------------------------

import arrow
import psycopg2
import evelink.map
import ConfigParser

# Configuration
config = ConfigParser.ConfigParser()
config.read(["config.ini"])
host = config.get("DATABASE", "host")
port = config.get("DATABASE", "port")
database = config.get("DATABASE", "database")
user = config.get("DATABASE", "user")
password = config.get("DATABASE", "password")

# Database connection
conn_string = "host=%s dbname=%s user=%s password=%s" % (host, database, user, password)

# API
mapapi = evelink.map.Map()
mapresponse = mapapi.kills_by_system()
jumpsapi = evelink.map.Map()
jumpresponse = jumpsapi.jumps_by_system()

# Convert timestamps to Arrow
mapapi_dataTime = arrow.get(mapresponse.timestamp)
mapapi_cachedUntil = arrow.get(mapresponse.expires)
jumps_dataTime = arrow.get(jumpresponse.timestamp)
jumps_cachedUntil = arrow.get(jumpresponse.expires)

# Get dictionary
mapapi_data = mapresponse.result[0]
jumpsapi_data = jumpresponse.result[0]

# Format timestamps
maptimestamp = mapapi_cachedUntil.format('YYYY-MM-DD HH:mm:ss')
jumpstimestamp = jumps_cachedUntil.format('YYYY-MM-DD HH:mm:ss')


#
# Map functions
#


def mapcheckrowexists(timestamp, id, ship, faction, pod):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT * FROM data."mapkills" WHERE timestamp = %s AND "mapkills"."solarSystemID" = %s AND "mapkills"."shipKills" = %s and "mapkills"."factionKills" = %s AND "mapkills"."podKills" = %s'
    data = (timestamp, id, ship, faction, pod, )
    cursor.execute(sql, data)
    result = cursor.fetchall()
    return result


def mapinsertrecord(timestamp, id, ship, faction, pod):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'INSERT INTO data."mapkills" (timestamp, "solarSystemID", "shipKills", "factionKills", "podKills") VALUES (%s, %s, %s, %s, %s)'
    data = (timestamp, id, ship, faction, pod, )
    cursor.execute(sql, data)
    conn.commit()
    return 0

def insertmap(mapapi_data):
    count_insert = 0
    for key,value in mapapi_data.iteritems():
        id = value['id']
        ship = value['ship']
        faction = value['faction']
        pod = value['pod']
        if len(mapcheckrowexists(maptimestamp, id, ship, faction, pod)) == 0:
            mapinsertrecord(maptimestamp, id, ship, faction, pod)
            count_insert += 1
    return count_insert


#
# Jumps functions
#


def jumpcheckrowexists(timestamp, id, jumps):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT * FROM data."mapjumps" WHERE timestamp = %s AND "mapjumps"."solarSystemID" = %s AND "mapjumps"."shipJumps" = %s'
    data = (timestamp, id, jumps, )
    cursor.execute(sql, data)
    result = cursor.fetchall()
    return result


def jumpsinsertrecord(timestamp, id, jumps):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'INSERT INTO data."mapjumps" (timestamp, "solarSystemID", "shipJumps") VALUES (%s, %s, %s)'
    data = (timestamp, id, jumps, )
    cursor.execute(sql, data)
    conn.commit()
    return 0


def insertjumps(jumps_data):
    count_insert = 0
    for key,value in jumpsapi_data.iteritems():
        id = key
        jumps = value
        if len(jumpcheckrowexists(jumpstimestamp, id, jumps)) == 0:
            jumpsinsertrecord(jumpstimestamp, id, jumps)
            count_insert += 1
    return count_insert


def main():
    # Run Map import
    count_mapinsert = insertmap(mapapi_data)
    print("[" + str(maptimestamp) + "][Informational] Map Inserted: " + str(count_mapinsert))

    # Run Jumps import
    count_jumpsinsert = insertjumps(jumpsapi_data)
    print("[" + str(jumpstimestamp) + "][Informational] Jumps Inserted: " + str(count_jumpsinsert))

if __name__ == "__main__":
    main()


