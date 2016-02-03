#############################
# Dependencies
#############################

import psycopg2
import ConfigParser
import time
import arrow
import pycrest
import pandas as pd
import fileinput
import sys

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
def getregions_byfaction(factionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = """SELECT
      "chrFactions"."factionName",
      "chrFactions"."factionID",
      "mapRegions"."regionName",
      "mapRegions"."regionID"
    FROM
      public."chrFactions",
      public."mapRegions"
    WHERE
      "mapRegions"."factionID" = "chrFactions"."factionID"
      AND "mapRegions"."factionID" = %s
    """
    data = (factionID, )
    cursor.execute(sql, data)
    df = pd.DataFrame(cursor.fetchall(),columns=['factionName','factionID','regionName','regionID'])
    cursor.close()
    return df


#
# Input     dataframe of a single region
# Output    dataframe of regions
#
def getnpckills_byregions(regions):
    df = pd.DataFrame()
    for region in regions:
        df_result = getnpckills_byregion(region)
        df = df.append(df_result)
    df.reset_index()
    return df


#
# Input     regionID
# Output    dataframe of SUM_factionKills grouped by timestamp
#
def getnpckills_byuniverse():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = """SELECT
      SUM(mapkills."factionKills") as SUM_factionKills, timestamp
    FROM
      data.mapkills
    GROUP BY mapkills."timestamp"
    ORDER BY timestamp DESC
    """
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall(),columns=['SUM_factionKills', 'timestamp'])
    df = df.set_index(['timestamp'])
    cursor.close()
    return df


#
# Input     none
# Output    dataframe of SUM_factionKills grouped by security
#
def getnpckills_byallsecurity():
    df = getnpckills_bysecurity(0.5, 1.0, 'high')
    df = df.combine_first(getnpckills_bysecurity(0.0, 0.5, 'low'))
    df = df.combine_first(getnpckills_bysecurity(-1, 0.0, 'null'))
    return df


def getnpckills_bysecurity(low, high, name):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = """SELECT
      SUM(mapkills."factionKills") as SUM_factionKills, timestamp
    FROM
      data.mapkills,
      public."mapSolarSystems"
    WHERE
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
     "mapSolarSystems"."security" BETWEEN %s AND %s
    GROUP BY mapkills."timestamp"
    ORDER BY timestamp DESC
    """
    data = (low, high, )
    cursor.execute(sql, data)
    df = pd.DataFrame(cursor.fetchall(),columns=[name, 'timestamp'])
    df = df.set_index(['timestamp'])
    cursor.close()
    return df


#
# Input     regionID
# Output    dataframe of SUM_factionKills grouped by timestamp
#
def getnpckills_byregion(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = """SELECT
      "mapSolarSystems"."regionID",
      "mapRegions"."regionName",
    SUM(mapkills."factionKills") as SUM_factionKills,
      mapkills."timestamp"
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapSolarSystems"."solarSystemID" = mapkills."solarSystemID" AND
      public."mapSolarSystems"."regionID" = %s
    GROUP BY mapkills."timestamp", public."mapSolarSystems"."regionID", "mapRegions"."regionName"
    ORDER BY timestamp DESC
    """
    data = (regionID, )
    cursor.execute(sql, data)
    df = pd.DataFrame(cursor.fetchall(),columns=['regionID', 'regionName', 'SUM_factionKills', 'timestamp'])
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
        if len(mapcheckrowexists(maptimestamp, id, ship, faction, pod)) == 0:
            mapinsertrecord(maptimestamp, id, ship, faction, pod)
            count_insert += 1
    return count_insert


#
# Check if map record exists
#
def mapcheckrowexists(timestamp, id, ship, faction, pod):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT * FROM data."mapkills" WHERE timestamp = %s AND "mapkills"."solarSystemID" = %s AND "mapkills"."shipKills" = %s and "mapkills"."factionKills" = %s AND "mapkills"."podKills" = %s'
    data = (timestamp, id, ship, faction, pod, )
    cursor.execute(sql, data)
    result = cursor.fetchall()
    return result


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
        if len(jumpcheckrowexists(jumpstimestamp, id, jumps)) == 0:
            jumpsinsertrecord(jumpstimestamp, id, jumps)
            count_insert += 1
    return count_insert


#
# Check if jump record exists
#
def jumpcheckrowexists(timestamp, id, jumps):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT * FROM data."mapjumps" WHERE timestamp = %s AND "mapjumps"."solarSystemID" = %s AND "mapjumps"."shipJumps" = %s'
    data = (timestamp, id, jumps, )
    cursor.execute(sql, data)
    result = cursor.fetchall()
    return result


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


#
# Input     CREST JSON
# Output    Database insert

def insertmarket(regionID, typeID, history):
    count = 0
    for row in history['items']:
        volume = row['volume']
        orderCount =  row['orderCount']
        lowPrice = row['lowPrice']
        highPrice = row['highPrice']
        avgPrice = row['avgPrice']
        timestamp = row['date']
        result = markethistorycheckrowexists(typeID, regionID, timestamp, volume, orderCount)
        if len(result) == 0:
            markethistoryinsertrecord(typeID, regionID, timestamp, volume, orderCount, lowPrice, highPrice, avgPrice)
            count += 1
    return count


#
# Check if markethistory record exists
#
def markethistorycheckrowexists(typeID, regionID, timestamp, volume, orderCount):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT * FROM data."markethistory" WHERE
          "markethistory"."typeID" = %s AND
          "markethistory"."regionID" = %s AND
          timestamp = %s AND
          "markethistory"."volume" = %s AND
          "markethistory"."orderCount" = %s'''
    data = (typeID, regionID, timestamp, volume, orderCount, )
    cursor.execute(sql, data)
    result = cursor.fetchall()
    return result


#
# Insert markethistory record
#
def markethistoryinsertrecord(typeID, regionID, timestamp, volume, orderCount, lowPrice, highPrice, avgPrice):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'INSERT INTO data."markethistory" ("typeID", "regionID", timestamp, "volume", "orderCount", "lowPrice", "highPrice", "avgPrice") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    data = (typeID, regionID, timestamp, volume, orderCount, lowPrice, highPrice, avgPrice, )
    cursor.execute(sql, data, )
    conn.commit()
    return 0


#
# Output list of ships by typeID
#
def getships():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      "invTypes"."typeID"
    FROM
      public."invTypes",
      public."invGroups"
    WHERE
      "invGroups"."groupID" = "invTypes"."groupID" AND
      "invGroups"."groupID" IN (26, 27, 234, 358, 380, 419, 420, 463, 513, 540, 541, 543, 830, 831, 832, 833, 834, 893, 894, 898, 900, 902, 906, 941, 963, 1022, 1201, 1202, 1305, 1527, 1534) AND
      "invTypes"."typeID" NOT IN (635, 4005, 34475, 34467, 4469, 34479, 34463, 34459, 34465, 34473, 34457, 34471, 34477, 34461, 34469, 11011, 1904, 25560, 1912, 1914, 1916, 1918, 26840, 33685, 33553, 33639, 33641, 33643, 33645, 33647, 33649, 33651, 33653, 34445, 11936, 11938, 13202, 33627, 33623, 33625, 33629, 33631, 33633, 33635, 33637, 34227, 33683, 34219, 34221, 34223, 34231, 34233, 34235, 34241, 34243, 34245, 34253, 34255, 34257, 34229, 34118, 34151, 34225, 34213, 34215, 34217, 34237, 34239, 34247, 34249, 34251, 34441, 26842, 32790, 32840, 32842, 32844, 32846, 32848, 33395, 33397, 33673, 33675, 33869, 33871, 33873, 33875, 33877, 33879, 33881, 33883, 35779, 35781)
      '''
    cursor.execute(sql, )
    result = cursor.fetchall() # Need to correct to return a list
    return result


#
# Input     regionIDs, typeIDs
# Output    database insert
#
def getmarkethistory(regionIDs, typeIDs):
    eve = pycrest.EVE()
    for regionID in regionIDs:
        for typeID in typeIDs:
            start_time = time.time()
            url = "https://public-crest.eveonline.com/market/" + str(regionID) + "/types/" + str(typeID) + "/history/"
            history = eve.get(url)
            count = insertmarket(regionID, typeID, history)
            timemark = arrow.get().to('US/Pacific').format('YYYY-MM-DD HH:mm:ss')
            log = "[" + str(timemark) + "][consumer_markethistory.py][insert:" + str(count) + " @ " + str(round(count/(time.time() - start_time), 2)) + " rec/sec][regionID:" + str(regionID) + "][typeID:" + str(typeID) + "]"
            print(log)
            with open("logs/consumer_markethistory.log", "a") as f:
                f.write(log + "\n")
    return 0


#
# Need to parametrize by security class
#
def gettoprattingsystems_nullsec():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapkills."solarSystemID",
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems"."security",
      SUM(mapkills."factionKills") AS SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      data.mapkills,
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
      "mapSolarSystems"."solarSystemID" = mapkills."solarSystemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapSolarSystems"."security" < 0.0
     GROUP BY mapkills."solarSystemID", "mapSolarSystems"."solarSystemName", "mapRegions"."regionName", "mapSolarSystems"."security"
     ORDER BY SUM(mapkills."factionKills") DESC'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['solarSystemID', 'solarSystemName', 'security', 'SUM_factionKills', 'regionName'])
    cursor.close()
    return df

#
# Need to parametrize by security class
#
def gettoprattingsystems_lowsec():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapkills."solarSystemID",
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems"."security",
      SUM(mapkills."factionKills") AS SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      data.mapkills,
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
      "mapSolarSystems"."solarSystemID" = mapkills."solarSystemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapSolarSystems"."security" BETWEEN 0.0 and 0.5
     GROUP BY mapkills."solarSystemID", "mapSolarSystems"."solarSystemName", "mapRegions"."regionName", "mapSolarSystems"."security"
     ORDER BY SUM(mapkills."factionKills") DESC'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['solarSystemID', 'solarSystemName', 'security', 'SUM_factionKills', 'regionName'])
    cursor.close()
    return df


#
# Need to parametrize by security class
#
def gettoprattingsystems_highsec():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapkills."solarSystemID",
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems"."security",
      SUM(mapkills."factionKills") AS SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      data.mapkills,
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
      "mapSolarSystems"."solarSystemID" = mapkills."solarSystemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapSolarSystems"."security" BETWEEN 0.5 and 1.0
     GROUP BY mapkills."solarSystemID", "mapSolarSystems"."solarSystemName", "mapRegions"."regionName", "mapSolarSystems"."security"
     ORDER BY SUM(mapkills."factionKills") DESC'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['solarSystemID', 'solarSystemName', 'security', 'SUM_factionKills', 'regionName'])
    cursor.close()
    return df


#
# Need to parametrize by security class
#
def gettoprattingregions_nullsec():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      SUM(mapkills."factionKills") as SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems".security < 0.0
    GROUP BY "mapRegions"."regionName"
    ORDER BY SUM_factionKills DESC'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['SUM_factionKills', 'regionName'])
    cursor.close()
    return df


#
# Need to parametrize by security class
#
def gettoprattingregions_lowsec():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      SUM(mapkills."factionKills") as SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems".security BETWEEN 0.0 and 0.5
    GROUP BY "mapRegions"."regionName"
    ORDER BY SUM_factionKills DESC'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['SUM_factionKills', 'regionName'])
    cursor.close()
    return df


#
# Need to parametrize by security class
#
def gettoprattingregions_highsec():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      SUM(mapkills."factionKills") as SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems".security BETWEEN 0.5 and 1.0
    GROUP BY "mapRegions"."regionName"
    ORDER BY SUM_factionKills DESC'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['SUM_factionKills', 'regionName'])
    cursor.close()
    return df


def getnpckills_bysecurity_bytime():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
       SUM(mapkills."factionKills") as SUM_factionKills,
       mapkills."timestamp",
      "mapRegions"."regionName"
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems".security < 0.0
    GROUP BY "mapRegions"."regionName", mapkills."timestamp"'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['SUM_factionKills', 'timestamp', 'regionName'])
    cursor.close()
    return df


#
# Input     dataframe.to_html
# Output    remove border=1
# pandas has a hard coded border=1
#
def cleartableborder(filename):
    for line in fileinput.FileInput(filename, inplace=1):
        line = line.replace('<table border="1" class="dataframe table table-striped">', '<table class="dataframe table table-striped">')
        sys.stdout.write(line)
    return 0

#
#
#
#
def addkillsperday(df):
    df['killsPerDay'] = df['SUM_factionKills'] / int(getdaterange_mapkills())
    return df


#
# Input table
# Output first and last timestamp
#
def getdaterange_mapkills():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      "timestamp"
    FROM
      data.mapkills
    ORDER BY "timestamp" ASC
    LIMIT 1'''
    cursor.execute(sql, )
    date_start = cursor.fetchone()

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      "timestamp"
    FROM
      data.mapkills
    ORDER BY "timestamp" DESC
    LIMIT 1'''
    cursor.execute(sql, )
    date_end = cursor.fetchone()

    return 18


def getsolarsystemmapkills(solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapkills."timestamp",
      mapkills."factionKills",
      mapkills."podKills",
      mapkills."shipKills"
    FROM
      data.mapkills
     WHERE mapkills."solarSystemID" = %s'''
    data = (solarSystemID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp', 'factionKills', 'podKills', 'shipKills'])
    df = df.set_index(['timestamp'])
    cursor.close()
    return df


def getsolarsystemmapjumps(solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapjumps."timestamp",
      mapjumps."shipJumps"
    FROM
      data.mapjumps
    WHERE "solarSystemID" = %s'''
    data = (solarSystemID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp', 'shipJumps'])
    df = df.set_index(['timestamp'])
    cursor.close()
    return df


#
# Insert sov data
#
def insertsov(sovapi_data, sovtimestamp):
    count_insert = 0
    for key,value in sovapi_data.iteritems():
        solarSystemID = value['id']
        allianceID = value['alliance_id']
        corporationID = value['corp_id']
        factionID = value['faction_id'] # Not used
        solarSystemName = value['name'] # Not used
        if str(allianceID) != "None":   # Filter out factions
            if getmaptopsov(solarSystemID) != corporationID:
                insertmapsov(sovtimestamp, allianceID, corporationID, solarSystemID)
                count_insert += 1
    return count_insert


#
# Get latest sov record
#
def getmaptopsov(solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapsov."corporationID"
    FROM
      data.mapsov
    WHERE mapsov."solarSystemID" = %s
    ORDER BY mapsov."timestamp" DESC
    LIMIT 1
    '''
    data = (solarSystemID, )
    cursor.execute(sql, data, )
    result = cursor.fetchone()
    if result == None:  # Error checking if table is empty
            return 0
    else:
        return result[0]


#
# Insert latest sov record
#
def insertmapsov(timestamp, allianceID, corporationID, solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'INSERT INTO data."mapsov" (timestamp, "allianceID", "corporationID", "solarSystemID") VALUES (%s, %s, %s, %s)'
    data = (timestamp, allianceID, corporationID, solarSystemID, )
    cursor.execute(sql, data)
    conn.commit()
    return 0



