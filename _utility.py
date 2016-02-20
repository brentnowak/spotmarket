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
import json
import sys

from psycopg2.extras import RealDictCursor

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
def regionName(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT "mapRegions"."regionName" FROM public."mapRegions" WHERE "mapRegions"."regionID" = %s'
    data = (regionID, )
    cursor.execute(sql, data, )
    results = json.dumps(cursor.fetchone(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


#
# Input     typeID
# Output    typeName
#
def typeName(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      "invTypes"."typeName"
    FROM
      public."invTypes"
      WHERE "invTypes"."typeID" = %s'''
    data = (typeID, )
    cursor.execute(sql, data, )
    results = json.dumps(cursor.fetchone(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


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
# Usage         consumer_map.py
# Input         mapapi_data, maptimestamp
# Output        'mapkills' Database insert
#
def insertkillsrecords(killsapi_data, maptimestamp):
    insertcount = 0
    for key,value in killsapi_data.iteritems():
        try:
            id = value['id']
            ship = value['ship']
            faction = value['faction']
            pod = value['pod']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            sql = 'INSERT INTO data."mapkills" (timestamp, "solarSystemID", "shipKills", "factionKills", "podKills") VALUES (%s, %s, %s, %s, %s)'
            data = (maptimestamp, id, ship, faction, pod, )
            cursor.execute(sql, data, )
        except psycopg2.IntegrityError:
            conn.rollback()
        else:
            conn.commit()
            insertcount += 1
    return insertcount


#
# Usage         consumer_map.py
# Input         jumpsapi_data, jumpstimestamp
# Output        'mapjumps' Database insert
#
def insertjumpsrecords(jumps_data, jumpstimestamp):
    insertcount = 0
    for key,value in jumps_data.iteritems():
        try:
            id = key
            jumps = value
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            sql = 'INSERT INTO data."mapjumps" (timestamp, "solarSystemID", "shipJumps") VALUES (%s, %s, %s)'
            data = (jumpstimestamp, id, jumps, )
            cursor.execute(sql, data, )
        except psycopg2.IntegrityError:
            conn.rollback()
        else:
            conn.commit()
            insertcount += 1
    return insertcount


#
# Usage         consumer_alliance.py
# Input         alliance_data
# Output        'alliances' Database insert
#
def insertalliancesrecords(alliance_data):
    insertcount = 0
    for key,value in alliance_data.iteritems():
        try:
            allianceID = value['id']
            ticker = value['ticker']
            name = value['name']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            sql = 'INSERT INTO data."alliances" ("allianceID", "ticker", "name") VALUES (%s, %s, %s)'
            data = (allianceID, ticker, name, )
            cursor.execute(sql, data, )
        except psycopg2.IntegrityError:
            conn.rollback()
        else:
            conn.commit()
            insertcount += 1
    return insertcount


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

def insertmarketrecord(regionID, typeID, history):
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
      "invGroups"."groupID" IN (1041)
      '''
    cursor.execute(sql, )
    result = cursor.fetchall() # Need to correct to return a list
    cursor.close()
    return result


#
# Input     regionIDs, typeIDs
# Output    database insert
#
def getmarkethistory(regionID, typeID):
    eve = pycrest.EVE()
    start_time = time.time()
    url = "https://public-crest.eveonline.com/market/" + str(regionID) + "/types/" + str(typeID) + "/history/"
    history = eve.get(url)
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


def gettradehubjumps(limit):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapjumps."timestamp",
      mapjumps."shipJumps",
      "mapSolarSystems"."solarSystemName"
    FROM
      data.mapjumps,
      public."mapSolarSystems"
    WHERE
      mapjumps."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      mapjumps."solarSystemID" IN (30000142, 30002187, 30002510, 30002659)
     ORDER BY mapjumps."timestamp" DESC
     LIMIT %s'''
    data = (limit, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp', 'shipJumps', 'solarSystemName'])
    df = df.set_index(['timestamp'])
    cursor.close()
    return df


def gettradehub_jitatoamarr(limit):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapjumps."timestamp",
      mapjumps."shipJumps",
      "mapSolarSystems"."solarSystemName"
    FROM
      data.mapjumps,
      public."mapSolarSystems"
    WHERE
      mapjumps."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      mapjumps."solarSystemID" IN (30000142, 30000144, 30000139, 30002791, 30002788, 30002789, 30003504, 30003503, 30003491, 30002187)
     ORDER BY mapjumps."timestamp" DESC
     LIMIT %s'''
    data = (limit, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp', 'shipJumps', 'solarSystemName'])
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
    conn.close()
    return 0


def getfactionkills_byfaction():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapkills."timestamp",
      SUM (mapkills."factionKills") AS SUM_factionKills
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."solarSystemID" = mapkills."solarSystemID" AND
      "mapRegions"."regionID" IN ('10000031', '10000056', '10000062', '10000061', '10000025', '10000012', '10000008', '10000006', '10000005', '10000009', '10000011', '10000014')
    GROUP BY mapkills."timestamp"
    ORDER BY mapkills."timestamp" DESC'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp', 'SUM_factionKills'])
    df = df.set_index(['timestamp'])
    conn.close()
    return df


#############################
# Market
#############################

def getmarkethistory_typeid(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      markethistory."typeID",
      "invTypes"."typeName",
      markethistory."regionID",
      to_char(markethistory."timestamp", 'YYYY-MM-dd') AS timestamp,
      markethistory.volume,
      markethistory."orderCount",
      markethistory."lowPrice",
      markethistory."highPrice",
      markethistory."avgPrice"
    FROM
      public."invTypes",
      data.markethistory
     WHERE markethistory."typeID" = "invTypes"."typeID" AND
     markethistory."typeID" = %s
     ORDER BY markethistory."timestamp" DESC'''
    data = (typeID, )
    cursor.execute(sql, data, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def getmarkethistory_d3_typeid(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      to_char(markethistory."timestamp", 'YYYY-MM-dd') AS timestamp,
      markethistory."lowPrice",
      markethistory."highPrice",
      markethistory."avgPrice"
    FROM
      data.markethistory
     WHERE markethistory."typeID" = %s
     ORDER BY markethistory."timestamp" DESC'''
    data = (typeID, )
    cursor.execute(sql, data, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


#############################
# Log File
#############################

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def getlog():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      *
    FROM
      data.logs
    ORDER BY logs."logID" DESC
    LIMIT 200
    '''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def insertlog(service, severity, detail, timestamp):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'INSERT INTO data."logs" (timestamp, "service", "severity", "detail") VALUES (%s, %s, %s, %s)'
    data = (timestamp, service, severity, detail, )
    cursor.execute(sql, data)
    conn.commit()
    return 0

def insertlog_timestamp(service, severity, detail, timestamp):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'INSERT INTO data."logs" (timestamp, "service", "severity", "detail") VALUES (to_timestamp(%s), %s, %s, %s)'
    data = (timestamp, service, severity, detail, )
    cursor.execute(sql, data)
    conn.commit()
    return 0


#############################
# Dashboard
#############################

def databasecountmapkills():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT COUNT(*) FROM data."mapkills"'
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def databasecountmapjumps():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT COUNT(*) FROM data."mapjumps"'
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def databasecountmapsov():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT COUNT(*) FROM data."mapsov"'
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def databasecountmarkethistory():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT COUNT(*) FROM data."markethistory"'
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def toprattingevents():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      mapkills."timestamp",
      SUM(mapkills."factionKills") AS SUM_factionKills,
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName"
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID"
    GROUP BY "mapSolarSystems"."solarSystemName", mapkills."timestamp", "mapRegions"."regionName"
    ORDER BY SUM_factionKills DESC
    LIMIT 30
    '''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def topnullrattingsystems():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      SUM(mapkills."factionKills") AS SUM_factionKills,
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems"."security",
      "mapRegions"."regionName"
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."security" < 0.0
    GROUP BY "mapSolarSystems"."solarSystemName", "mapSolarSystems"."security", "mapRegions"."regionName"
    ORDER BY SUM_factionKills DESC
    LIMIT 30
    '''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def topnullrattingregions():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      SUM(mapkills."factionKills") AS SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."security" < 0.0
    GROUP BY "mapRegions"."regionName"
    ORDER BY SUM_factionKills DESC
    LIMIT 30
    '''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


#############################
# factionReport
#############################


def getregionrecordtimestamps():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
    mapkills."timestamp"
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapRegions"."regionID" IN ('10000031', '10000056', '10000062', '10000061', '10000025', '10000012', '10000008', '10000006', '10000005', '10000009', '10000011', '10000014')
    GROUP BY mapkills."timestamp"
    ORDER BY mapkills."timestamp" DESC
    LIMIT 20'''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def indexrattingbyfactionkills():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      SUM(mapkills."factionKills") as SUM_factionKills,
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems"."solarSystemID",
      "mapRegions"."regionName"
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."security" < 0.0
    GROUP BY "mapSolarSystems"."solarSystemName", "mapSolarSystems"."solarSystemID", "mapRegions"."regionName"
    ORDER BY SUM_factionKills DESC
    '''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['SUM_factionKills', 'solarSystemName', 'solarSystemID', 'regionID'])
    df = df.set_index(['solarSystemID'])
    cursor.close()
    return df


def indexrattingbyjumps():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      SUM(mapjumps."shipJumps") as SUM_shipJumps,
      "mapSolarSystems"."solarSystemID"
    FROM
      data.mapjumps,
      public."mapSolarSystems"
    WHERE
      mapjumps."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."security" < 0.0
    GROUP BY "mapSolarSystems"."solarSystemID"
    ORDER BY SUM_shipJumps ASC
    '''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['SUM_shipJumps', 'solarSystemID'])
    df = df.set_index(['solarSystemID'])
    cursor.close()
    return df


def indexrattingbyshipkills():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      SUM(mapkills."shipKills") as SUM_shipKills,
      "mapSolarSystems"."solarSystemID"
    FROM
      data.mapkills,
      public."mapSolarSystems"
    WHERE
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."security" < 0.0
    GROUP BY "mapSolarSystems"."solarSystemID"
    ORDER BY SUM_shipKills ASC
    '''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['SUM_shipKills', 'solarSystemID'])
    df = df.set_index(['solarSystemID'])
    cursor.close()
    return df


def indexrattingbypodkills():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      SUM(mapkills."podKills") as SUM_podKills,
      "mapSolarSystems"."solarSystemID"
    FROM
      data.mapkills,
      public."mapSolarSystems"
    WHERE
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."security" < 0.0
    GROUP BY "mapSolarSystems"."solarSystemID"
    ORDER BY SUM_podKills ASC
    '''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['SUM_podKills', 'solarSystemID'])
    df = df.set_index(['solarSystemID'])
    cursor.close()
    return df


def indexsolarsystemgatecount():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      "mapSolarSystemJumps"."fromSolarSystemID" as solarSystemID,
      COUNT(*) as gateCount
    FROM
      public."mapSolarSystemJumps"
     GROUP BY solarSystemID
    '''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['solarSystemID', 'gateCount'])
    df = df.set_index(['solarSystemID'])
    cursor.close()
    return df


def indexrattinguniverse():
    df1 = indexrattingbyfactionkills()
    df2 = indexrattingbyjumps()
    df3 = indexrattingbyshipkills()
    df4 = indexrattingbypodkills()
    df5 = indexsolarsystemgatecount()

    df1 = df1.combine_first(df2)
    df1 = df1.combine_first(df3)
    df1 = df1.combine_first(df4)
    df1 = df1.combine_first(df5)

    df1['safetyIndex'] = 100
    df1 = df1.sort_values(by='SUM_factionKills', ascending=False)
    df1 = df1.head(30)
    return df1


def rattinghistorytopsystemsbyregion(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapkills."solarSystemID",
      SUM(mapkills."factionKills") as SUM_factionKills
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."solarSystemID" = mapkills."solarSystemID" AND
      "mapSolarSystems"."regionID" = %s
    GROUP BY
     mapkills."solarSystemID"
    ORDER BY SUM_factionKills DESC
    LIMIT 20'''
    data = (regionID, )
    cursor.execute(sql, data, )
    results = cursor.fetchall()
    cursor.close()
    return results


def rattinghistorybyregion(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapkills."timestamp",
      mapkills."factionKills",
      mapkills."solarSystemID",
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName"
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."solarSystemID" = mapkills."solarSystemID" AND
      "mapSolarSystems"."regionID" = %s
    GROUP BY mapkills."timestamp",
     mapkills."factionKills",
     mapkills."solarSystemID",
     "mapSolarSystems"."solarSystemName",
     "mapRegions"."regionName"
    '''
    data = (regionID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp', 'factionKills', 'solarSystemID', 'solarSystemName', 'regionName'])
    df = df.set_index(['timestamp'])
    cursor.close()
    return df


def rattinghistorybysystem(solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapkills."timestamp",
      mapkills."factionKills",
      mapkills."solarSystemID",
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName"
    FROM
      data.mapkills,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."solarSystemID" = mapkills."solarSystemID" AND
      "mapSolarSystems"."solarSystemID" = %s
    GROUP BY mapkills."timestamp",
     mapkills."factionKills",
     mapkills."solarSystemID",
     "mapSolarSystems"."solarSystemName",
     "mapRegions"."regionName"
    '''
    data = (solarSystemID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp', 'factionKills', 'solarSystemID', 'solarSystemName', 'regionName'])
    df = df.set_index(['timestamp'])
    cursor.close()
    return df

#############################
# Settings
#############################

def databasemarketitems():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      marketitems."typeID",
      "invTypes"."typeName",
      "invMarketGroups"."marketGroupName",
      marketitems.enabled,
      marketitems."importResult",
      marketitems."importTimestamp"
    FROM
      data.marketitems,
      public."invTypes",
      public."invMarketGroups"
    WHERE
      marketitems."typeID" = "invTypes"."typeID" AND
      "invTypes"."marketGroupID" = "invMarketGroups"."marketGroupID"
    '''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results



#############################
# Wallet
#############################

def getwallettransactions():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      wallet."transactionDateTime",
      wallet."transactionID",
      wallet."typeID",
      wallet."typeName",
      wallet.quantity,
      wallet.price,
      wallet."clientName",
      wallet."stationID",
      wallet."stationName",
      wallet."transactionType",
      wallet.personal,
      wallet.profit
    FROM
      data.wallet
    ORDER BY wallet."transactionDateTime" DESC
    '''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def getcharacters():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      *
    FROM
      data.characters'''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def insertwallettransaction(transactionDateTime, transactionID, quantity, typeName, typeID, price, clientID, clientName, walletID, stationID, stationName, transactionType, personal, profit):
    insertcount = 0
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        sql = '''INSERT INTO data.wallet(
            "transactionDateTime",
            "transactionID",
            quantity,
            "typeName",
            "typeID",
            price,
            "clientID",
            "clientName",
            "walletID",
            "stationID",
            "stationName",
            "transactionType",
            personal,
            profit)
        VALUES (to_timestamp(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        data = (transactionDateTime, transactionID, quantity, typeName, typeID, price, clientID, clientName, walletID, stationID, stationName, transactionType, personal, profit, )
        cursor.execute(sql, data)
    except psycopg2.IntegrityError:
        conn.rollback()
    else:
        conn.commit()
        insertcount += 1
    return insertcount


#############################
# sovereignty
#############################

def getsovevents():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      to_char(mapsov."timestamp", 'YYYY-MM-dd HH:mm:ss') AS timestamp,
      mapsov."solarSystemID",
      mapsov."allianceID",
      mapsov."corporationID",
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName",
      alliances.name AS allianceName,
      alliances.ticker
    FROM
      data.mapsov,
      data.alliances,
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
        mapsov."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
        mapsov."allianceID" = alliances."allianceID" AND
        "mapRegions"."regionID" = "mapSolarSystems"."regionID"
    ORDER BY mapsov."timestamp" DESC
    '''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


#############################
# regionReport
#############################

def getsovbyregion(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      "mapSolarSystems"."solarSystemID",
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems".security,
      mapsov."allianceID",
      alliances.ticker,
      alliances.name
    FROM
      data.alliances,
      public."mapSolarSystems",
      data.mapsov,
      public."mapRegions"
    WHERE
      "mapSolarSystems"."solarSystemID" = mapsov."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      mapsov."allianceID" = alliances."allianceID" AND
      "mapRegions"."regionID" = %s
    '''
    data = (regionID, )
    cursor.execute(sql, data, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results

def getrattingbyregion(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''
        SELECT
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems".security,
      alliances.ticker,
      alliances.name,
      mapsov."allianceID",
      SUM(mapkills."factionKills") as SUM_factionKills,
      mapkills."timestamp"
    FROM
      data.alliances,
      public."mapSolarSystems",
      data.mapsov,
      data.mapkills
    WHERE
      "mapSolarSystems"."solarSystemID" = mapsov."solarSystemID" AND
      mapsov."allianceID" = alliances."allianceID" AND
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = %s
    GROUP BY
      mapkills."solarSystemID", "mapSolarSystems"."solarSystemName", "mapSolarSystems".security,  alliances.ticker, alliances.name, mapsov."allianceID", mapkills."timestamp"
    '''
    data = (regionID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['solarSystemName', 'security', 'ticker', 'name', 'allianceID', 'SUM_factionKills', 'timestamp'])
    df = df.set_index(['timestamp'])
    cursor.close()
    return df

def gettoprattingbyregion(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''
        SELECT
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems".security,
      alliances.ticker,
      alliances.name,
      mapsov."allianceID",
      SUM(mapkills."factionKills") as SUM_factionKills
    FROM
      data.alliances,
      public."mapSolarSystems",
      data.mapsov,
      data.mapkills
    WHERE
      "mapSolarSystems"."solarSystemID" = mapsov."solarSystemID" AND
      mapsov."allianceID" = alliances."allianceID" AND
      mapkills."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = %s
    GROUP BY
      mapkills."solarSystemID", "mapSolarSystems"."solarSystemName", "mapSolarSystems".security,  alliances.ticker, alliances.name, mapsov."allianceID"
    '''
    data = (regionID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['solarSystemName', 'security', 'ticker', 'name', 'allianceID', 'SUM_factionKills'])
    cursor.close()
    return df


#############################
# moonReport
#############################

def getmoonmineralsbyregion(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      moonminerals."moonID",
      "mapDenormalize"."itemName",
      "invTypes"."typeID",
      "invTypes"."typeName",
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems".security,
      "mapRegions"."regionName",
      mapsov."allianceID",
      alliances.name,
      alliances.ticker
    FROM
      data.moonminerals,
      public."mapDenormalize",
      public."invTypes",
      public."mapSolarSystems",
      public."mapRegions",
      data.alliances,
      data.mapsov
    WHERE
      "mapDenormalize"."itemID" = moonminerals."moonID" AND
      "invTypes"."typeID" = moonminerals."typeID" AND
      "mapSolarSystems"."solarSystemID" = "mapDenormalize"."solarSystemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      alliances."allianceID" = mapsov."allianceID" AND
      mapsov."solarSystemID" = "mapDenormalize"."solarSystemID" AND
      "mapRegions"."regionID" = %s
    '''
    data = (regionID, )
    cursor.execute(sql, data, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def getmoonmineralsbytypeid(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      moonminerals."moonID",
      "mapDenormalize"."itemName",
      "invTypes"."typeID",
      "invTypes"."typeName",
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems".security,
      "mapRegions"."regionName",
      mapsov."allianceID",
      alliances.name,
      alliances.ticker
    FROM
      data.moonminerals,
      public."mapDenormalize",
      public."invTypes",
      public."mapSolarSystems",
      public."mapRegions",
      data.alliances,
      data.mapsov
    WHERE
      "mapDenormalize"."itemID" = moonminerals."moonID" AND
      "invTypes"."typeID" = moonminerals."typeID" AND
      "mapSolarSystems"."solarSystemID" = "mapDenormalize"."solarSystemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      alliances."allianceID" = mapsov."allianceID" AND
      mapsov."solarSystemID" = "mapDenormalize"."solarSystemID" AND
      "invTypes"."typeID" = %s
    '''
    data = (typeID, )
    cursor.execute(sql, data, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results

def getmoonmineralsbyalliance(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
    COUNT(moonminerals."moonID") as SUM_moonID,
      alliances.name
    FROM
      data.moonminerals,
      public."mapDenormalize",
      public."invTypes",
      public."mapSolarSystems",
      public."mapRegions",
      data.alliances,
      data.mapsov
    WHERE
      "mapDenormalize"."itemID" = moonminerals."moonID" AND
      "invTypes"."typeID" = moonminerals."typeID" AND
      "mapSolarSystems"."solarSystemID" = "mapDenormalize"."solarSystemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      alliances."allianceID" = mapsov."allianceID" AND
      mapsov."solarSystemID" = "mapDenormalize"."solarSystemID" AND
      "invTypes"."typeID" = %s
    GROUP BY
      alliances.name,
      alliances.ticker
    ORDER BY
      SUM_moonID DESC'''
    data = (typeID, )
    cursor.execute(sql, data, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results

def getmoonmineralsbysov():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
    COUNT(moonminerals."moonID") as SUM_moonID,
      alliances.name
    FROM
      data.moonminerals,
      public."mapDenormalize",
      public."invTypes",
      public."mapSolarSystems",
      public."mapRegions",
      data.alliances,
      data.mapsov
    WHERE
      "mapDenormalize"."itemID" = moonminerals."moonID" AND
      "invTypes"."typeID" = moonminerals."typeID" AND
      "mapSolarSystems"."solarSystemID" = "mapDenormalize"."solarSystemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      alliances."allianceID" = mapsov."allianceID" AND
      mapsov."solarSystemID" = "mapDenormalize"."solarSystemID"
    GROUP BY
      alliances.name,
      alliances.ticker
    ORDER BY
      SUM_moonID DESC'''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results