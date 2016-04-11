#############################
# Dependencies
#############################

import psycopg2
import ConfigParser
import time
import arrow
import pycrest
import pandas as pd
import json

from psycopg2.extras import RealDictCursor
from _globals import *

#############################
# Database
#############################

config = ConfigParser.ConfigParser()
config.read(["config.ini"]) #  For running on Windows
#config.read(["/home/ubuntu/spotmarket/config.ini"]) #  Full path needed for supervisor
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
def getregionName(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'SELECT "mapRegions"."regionName" FROM public."mapRegions" WHERE "mapRegions"."regionID" = %s'
    data = (regionID, )
    cursor.execute(sql, data, )
    results = cursor.fetchone()
    return results[0]


#
# Input     typeID
# Output    typeName as JSON
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
# Input     typeID
# Output    typeName
#
def gettypeName(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      "invTypes"."typeName"
    FROM
      public."invTypes"
      WHERE "invTypes"."typeID" = %s'''
    data = (typeID, )
    cursor.execute(sql, data, )
    results = cursor.fetchone()
    return results[0]


#
# Input     solarSystemID
# Output    solarSystemName
#
def getSolarSystemName(solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      "mapSolarSystems"."solarSystemName"
    FROM
      public."mapSolarSystems"
      WHERE "mapSolarSystems"."solarSystemID" = %s'''
    data = (solarSystemID, )
    cursor.execute(sql, data, )
    results = cursor.fetchone()
    return results[0]


# Input
# Output    Tuple of typeIDs
def gettypeIDsfromGroupID(groupID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      "invTypes"."typeID"
    FROM
      public."invTypes"
    WHERE "invTypes"."groupID" = %s'''
    data = (groupID, )
    cursor.execute(sql, data, )
    results = cursor.fetchall()
    return tuple(results)


#
# Input     moonName
# Output    moonID
#
def getmoonIDfromName(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      "mapDenormalize"."itemID"
    FROM
      public."mapDenormalize"
    WHERE "mapDenormalize"."itemName" = %s'''
    data = (typeID, )
    cursor.execute(sql, data, )
    results = cursor.fetchone()
    return results[0]

def gettypeiddetails(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      "invTypes"."typeName",
      "invMetaTypes"."metaGroupID",
      "invMetaGroups"."metaGroupName",
      "invTypes".volume
    FROM
      public."invTypes",
      public."invMetaTypes",
      public."invMetaGroups"
    WHERE
      "invTypes"."typeID" = "invMetaTypes"."typeID" AND
      "invMetaGroups"."metaGroupID" = "invMetaTypes"."metaGroupID" AND
      "invTypes"."typeID" = %s'''
    data = (typeID,)
    cursor.execute(sql, data, )
    results = cursor.fetchall()
    return results[0]


#
# Input     getnpckills_byregions
# Output    JSON of every faction region
#
def getnpckills_byallfactions():
    df = getnpckills_byregions(regions_angel, "Angel Cartel")
    df = df.combine_first(getnpckills_byregions(regions_blood, "Blood Raiders"))
    df = df.combine_first(getnpckills_byregions(regions_guristas, "Guristas"))
    df = df.combine_first(getnpckills_byregions(regions_sanshas, "Sansha's Nation"))
    df = df.combine_first(getnpckills_byregions(regions_serpentis, "Serpentis"))
    return df.reset_index().to_json(orient='records',date_format='iso')

def getnpckills_bywar(warName):
    if warName == "worldwarbee":
        df = getnpckills_byregions((10000023, ), "Pure Blind")
        df = df.combine_first(getnpckills_byregions((10000010, ), "Tribute"))
        df = df.combine_first(getnpckills_byregions((10000003, ), "Vale of the Silent"))
        df = df.combine_first(getnpckills_byregions((10000015,), "Venal"))
        return df.reset_index().to_json(orient='records', date_format='iso')
    else:
        return "No Data"

#
# Input     regions
# Output    dataframe of SUM_factionKills grouped by timestamp
#
def getnpckills_byregions(regions, factionName):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
    SUM(kill."factionKills") as factionKills,
      kill."timestamp"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapSolarSystems"."solarSystemID" = kill."solarSystemID" AND
      public."mapSolarSystems"."regionID" IN %s AND
      timestamp < TIMESTAMP 'yesterday'
    GROUP BY kill."timestamp"
    ORDER BY timestamp DESC
    '''
    data = (regions, )
    cursor.execute(sql, data)
    df = pd.DataFrame(cursor.fetchall(),columns=[factionName, 'timestamp'])
    df = df.set_index(['timestamp'])
    df = df.resample("12H",how='sum')
    cursor.close()
    return df


def getnpckills_byfaction(regions):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
    SUM(kill."factionKills") as factionKills,
      kill."timestamp",
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapSolarSystems"."solarSystemID" = kill."solarSystemID" AND
      public."mapSolarSystems"."regionID" IN %s AND
      timestamp < TIMESTAMP 'yesterday'
    GROUP BY kill."timestamp", "mapRegions"."regionName"
    ORDER BY timestamp DESC'''
    data = (regions,)
    cursor.execute(sql, data)
    df = pd.DataFrame(cursor.fetchall(), columns=['factionKills', 'timestamp', 'regionName'])
    df = pd.pivot_table(df, index='timestamp', columns='regionName', values='factionKills')
    df = df.resample("12H", how='sum')
    cursor.close()
    return df.reset_index().to_json(orient='records',date_format='iso')

#
# Input     regionID
# Output    dataframe of SUM_factionKills grouped by timestamp
#
def getnpckills_byuniverse():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = """SELECT
      SUM(kill."factionKills") as factionKills, timestamp
    FROM
      map.kill
    WHERE
      timestamp < TIMESTAMP 'yesterday'
    GROUP BY kill."timestamp"
    ORDER BY timestamp DESC
    """
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall(),columns=['factionKills', 'timestamp'])
    df = df.set_index(['timestamp'])
    df = df.resample("12H",how='sum')
    cursor.close()
    return df.reset_index().to_json(orient='records',date_format='iso')


#
# Input     none
# Output    dataframe of SUM_factionKills grouped by security
#
def getnpckills_byallsecurity():
    df = getnpckills_bysecurity(0.5, 1.0, 'high')
    df = df.combine_first(getnpckills_bysecurity(0.0, 0.5, 'low'))
    df = df.combine_first(getnpckills_bysecurity(-1, 0.0, 'null'))
    df = df.resample("12H",how='sum')
    return df.reset_index().to_json(orient='records',date_format='iso')


def getnpckills_bysecurity(low, high, name):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = """SELECT
      SUM(kill."factionKills") as SUM_factionKills, timestamp
    FROM
      map.kill,
      public."mapSolarSystems"
    WHERE
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
     "mapSolarSystems"."security" BETWEEN %s AND %s AND
      timestamp < TIMESTAMP 'yesterday'
    GROUP BY kill."timestamp"
    ORDER BY timestamp DESC
    """
    data = (low, high, )
    cursor.execute(sql, data)
    df = pd.DataFrame(cursor.fetchall(),columns=[name, 'timestamp'])
    df = df.set_index(['timestamp'])
    cursor.close()
    return df


#
# Regional Reports by Name
# "The North", "The South"
#
def getnpckills_byregionsname(regions, regionName):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
    SUM(kill."factionKills") as factionKills,
      kill."timestamp"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapSolarSystems"."solarSystemID" = kill."solarSystemID" AND
      public."mapSolarSystems"."regionID" IN %s AND
      timestamp < TIMESTAMP 'yesterday'
    GROUP BY kill."timestamp"
    ORDER BY timestamp DESC
    '''
    data = (regions, )
    cursor.execute(sql, data)
    df = pd.DataFrame(cursor.fetchall(),columns=[regionName, 'timestamp'])
    df = df.set_index(['timestamp'])
    df = df.resample("12H",how='sum')
    cursor.close()
    return df.reset_index().to_json(orient='records', date_format='iso')


def getjumps_byregionsname(regions, regionName):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
    SUM(mapjumps."shipJumps") as shipJumps,
      mapjumps."timestamp"
    FROM
      data.mapjumps,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapSolarSystems"."solarSystemID" = mapjumps."solarSystemID" AND
      public."mapSolarSystems"."regionID" IN %s AND
      timestamp < TIMESTAMP 'yesterday'
    GROUP BY mapjumps."timestamp"
    ORDER BY timestamp DESC
    '''
    data = (regions, )
    cursor.execute(sql, data)
    df = pd.DataFrame(cursor.fetchall(),columns=[regionName, 'timestamp'])
    df = df.set_index(['timestamp'])
    df = df.resample("12H",how='sum')
    cursor.close()
    return df.reset_index().to_json(orient='records', date_format='iso')


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
# Input     None
# Output    df
#
def gettoprattingsystems_nullsec(): # TODO Need to parametrize by security class
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      kill."solarSystemID",
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems"."security",
      SUM(kill."factionKills") AS SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
      "mapSolarSystems"."solarSystemID" = kill."solarSystemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapSolarSystems"."security" < 0.0
     GROUP BY kill."solarSystemID", "mapSolarSystems"."solarSystemName", "mapRegions"."regionName", "mapSolarSystems"."security"
     ORDER BY SUM(kill."factionKills") DESC'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['solarSystemID', 'solarSystemName', 'security', 'SUM_factionKills', 'regionName'])
    cursor.close()
    return df

#
# Input     None
# Output    df
#
def gettoprattingsystems_lowsec(): # TODO Need to parametrize by security class
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      kill."solarSystemID",
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems"."security",
      SUM(kill."factionKills") AS SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
      "mapSolarSystems"."solarSystemID" = kill."solarSystemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapSolarSystems"."security" BETWEEN 0.0 and 0.5
     GROUP BY kill."solarSystemID", "mapSolarSystems"."solarSystemName", "mapRegions"."regionName", "mapSolarSystems"."security"
     ORDER BY SUM(kill."factionKills") DESC'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['solarSystemID', 'solarSystemName', 'security', 'SUM_factionKills', 'regionName'])
    cursor.close()
    return df


#
# Input     None
# Output    df
#
def gettoprattingsystems_highsec(): # TODO Need to parametrize by security class
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      kill."solarSystemID",
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems"."security",
      SUM(kill."factionKills") AS SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
      "mapSolarSystems"."solarSystemID" = kill."solarSystemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapSolarSystems"."security" BETWEEN 0.5 and 1.0
     GROUP BY kill."solarSystemID", "mapSolarSystems"."solarSystemName", "mapRegions"."regionName", "mapSolarSystems"."security"
     ORDER BY SUM(kill."factionKills") DESC'''
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
      SUM(kill."factionKills") as SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
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
      SUM(kill."factionKills") as SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
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
      SUM(kill."factionKills") as SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
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
       SUM(kill."factionKills") as SUM_factionKills,
       kill."timestamp",
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems".security < 0.0
    GROUP BY "mapRegions"."regionName", kill."timestamp"'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['SUM_factionKills', 'timestamp', 'regionName'])
    cursor.close()
    return df

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
      map.kill
    ORDER BY "timestamp" ASC
    LIMIT 1'''
    cursor.execute(sql, )
    date_start = cursor.fetchone()

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      "timestamp"
    FROM
      map.kill
    ORDER BY "timestamp" DESC
    LIMIT 1'''
    cursor.execute(sql, )
    date_end = cursor.fetchone()

    return 49


def getsolarsystemmapkills(solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      kill."timestamp",
      kill."factionKills",
      kill."podKills",
      kill."shipKills"
    FROM
      map.kill
     WHERE kill."solarSystemID" = %s'''
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


def getfactionkills_byfaction():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      kill."timestamp",
      SUM (kill."factionKills") AS SUM_factionKills
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."solarSystemID" = kill."solarSystemID" AND
      "mapRegions"."regionID" IN ('10000031', '10000056', '10000062', '10000061', '10000025', '10000012', '10000008', '10000006', '10000005', '10000009', '10000011', '10000014')
    GROUP BY kill."timestamp"
    ORDER BY kill."timestamp" DESC'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp', 'SUM_factionKills'])
    df = df.set_index(['timestamp'])
    conn.close()
    return df


#############################
# Log File
#############################

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def getsystemlogs():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      to_char(log."timestamp", 'YYYY-MM-dd HH:mm:ss') AS timestamp,
      log."logID",
      log.service,
      log.severity,
      log.detail
    FROM
      system.log
    ORDER BY log."timestamp" DESC
    LIMIT 500
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
    sql = 'INSERT INTO system.log (timestamp, "service", "severity", "detail") VALUES (%s, %s, %s, %s)'
    data = (timestamp, service, severity, detail, )
    cursor.execute(sql, data)
    conn.commit()
    return 0


def insertlog_timestamp(service, severity, detail, timestamp):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'INSERT INTO system.log (timestamp, "service", "severity", "detail") VALUES (%s, %s, %s, %s)'
    data = (timestamp, service, severity, detail, )
    cursor.execute(sql, data)
    conn.commit()
    return 0


def toprattingevents():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      kill."timestamp",
      SUM(kill."factionKills") AS SUM_factionKills,
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID"
    GROUP BY "mapSolarSystems"."solarSystemName", kill."timestamp", "mapRegions"."regionName"
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
      SUM(kill."factionKills") AS SUM_factionKills,
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems"."security",
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
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
      SUM(kill."factionKills") AS SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
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
    kill."timestamp"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapRegions"."regionID" IN ('10000031', '10000056', '10000062', '10000061', '10000025', '10000012', '10000008', '10000006', '10000005', '10000009', '10000011', '10000014')
    GROUP BY kill."timestamp"
    ORDER BY kill."timestamp" DESC
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
      SUM(kill."factionKills") as SUM_factionKills,
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems"."solarSystemID",
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
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
      SUM(kill."shipKills") as SUM_shipKills,
      "mapSolarSystems"."solarSystemID"
    FROM
      map.kill,
      public."mapSolarSystems"
    WHERE
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
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
      SUM(kill."podKills") as SUM_podKills,
      "mapSolarSystems"."solarSystemID"
    FROM
      map.kill,
      public."mapSolarSystems"
    WHERE
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
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
      kill."solarSystemID",
      SUM(kill."factionKills") as SUM_factionKills
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."solarSystemID" = kill."solarSystemID" AND
      "mapSolarSystems"."regionID" = %s
    GROUP BY
     kill."solarSystemID"
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
      kill."timestamp",
      kill."factionKills",
      kill."solarSystemID",
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."solarSystemID" = kill."solarSystemID" AND
      "mapSolarSystems"."regionID" = %s
    GROUP BY kill."timestamp",
     kill."factionKills",
     kill."solarSystemID",
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
      kill."timestamp",
      kill."factionKills",
      kill."solarSystemID",
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."solarSystemID" = kill."solarSystemID" AND
      "mapSolarSystems"."solarSystemID" = %s
    GROUP BY kill."timestamp",
     kill."factionKills",
     kill."solarSystemID",
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

def getmarketitems():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      tracking."typeID",
      tracking."typeID" as "iconID",
      "invTypes"."typeName",
      "invMarketGroups"."marketGroupName",
      tracking.enabled,
      tracking."importResult",
      tracking."importTimestamp"
    FROM
      market.tracking,
      public."invTypes",
      public."invMarketGroups"
    WHERE
      tracking."typeID" = "invTypes"."typeID" AND
      "invTypes"."marketGroupID" = "invMarketGroups"."marketGroupID"
    '''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def getzkillboarditems():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      tracking."typeID" as "iconID",
      tracking."typeID",
      "invTypes"."typeName",
      "invMarketGroups"."marketGroupName",
      tracking.enabled,
      tracking."lastPage",
      tracking."importResult",
      tracking."importTimestamp"
    FROM
      kill.tracking,
      public."invTypes",
      public."invMarketGroups"
    WHERE
      tracking."typeID" = "invTypes"."typeID" AND
      "invTypes"."marketGroupID" = "invMarketGroups"."marketGroupID"
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
      "walletID",
      "characterID",
      "characterID" as "iconID",
      "characterName",
      "keyID",
      "vCode",
      RIGHT("vCode", 6) as "trunkCode",
      "enableWallet", "enableJournal", "enableOrders", "enableBlueprints",
      "displayWallet", "displayOrders", "displayBlueprints", "corpKey"
    FROM
      "character".characters'''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


#############################
# sovereignty
#############################

def getsovevents():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      to_char(sov."timestamp", 'YYYY-MM-dd HH:mm:ss') AS timestamp,
      sov."solarSystemID",
      sov."allianceID",
      sov."corporationID",
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName",
      alliances.name AS allianceName,
      alliances.ticker
    FROM
      map.sov,
      meta.alliances,
      public."mapSolarSystems",
      public."mapRegions"
    WHERE
        sov."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
        sov."allianceID" = alliances."allianceID" AND
        "mapRegions"."regionID" = "mapSolarSystems"."regionID"
    ORDER BY sov."timestamp" DESC
    '''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    cursor.close()
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def getsoveventsumbyday():  # TODO remove hard coded date start, scrape Dotlan for sov history
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''
    SELECT date_trunc('day', timestamp) AS timestamp,
        COUNT(*) AS sovChange
        FROM map.sov
        WHERE timestamp >= DATE('2016-02-03')
        GROUP BY date_trunc('day', timestamp)
        ORDER BY timestamp DESC'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp','sovchange'])
    cursor.close()
    df = df.set_index(['timestamp'])
    return df.reset_index().to_json(orient='records',date_format='iso')


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
      meta.alliances,
      public."mapSolarSystems",
      map.sov,
      public."mapRegions"
    WHERE
      "mapSolarSystems"."solarSystemID" = sov."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      sov."allianceID" = alliances."allianceID" AND
      "mapRegions"."regionID" = %s
    '''
    data = (regionID, )
    cursor.execute(sql, data, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    cursor.close()
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
      SUM(kill."factionKills") as SUM_factionKills,
      kill."timestamp"
    FROM
      meta.alliances,
      public."mapSolarSystems",
      data.mapsov,
      map.kill
    WHERE
      "mapSolarSystems"."solarSystemID" = mapsov."solarSystemID" AND
      mapsov."allianceID" = alliances."allianceID" AND
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = %s
    GROUP BY
      kill."solarSystemID", "mapSolarSystems"."solarSystemName", "mapSolarSystems".security,  alliances.ticker, alliances.name, mapsov."allianceID", kill."timestamp"
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
      SUM(kill."factionKills") as SUM_factionKills
    FROM
      meta.alliances,
      public."mapSolarSystems",
      data.mapsov,
      map.kill
    WHERE
      "mapSolarSystems"."solarSystemID" = mapsov."solarSystemID" AND
      mapsov."allianceID" = alliances."allianceID" AND
      kill."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = %s
    GROUP BY
      kill."solarSystemID", "mapSolarSystems"."solarSystemName", "mapSolarSystems".security,  alliances.ticker, alliances.name, mapsov."allianceID"
    '''
    data = (regionID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['solarSystemName', 'security', 'ticker', 'name', 'allianceID', 'SUM_factionKills'])
    cursor.close()
    return df


def getkillmailsbyregion(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''
    SELECT
      killmails."killData"->'killTime' as timestamp,
      killmails."killID",
      killmails."killHash",
      killmails."totalValue",
      killmails."killData"->'attackerCount' as attackerCount,
      killmails."killData"->'victim'->'damageTaken' as damageTaken,
      killmails."killData"->'victim'->'alliance'->'name' as allianceName,
      (killmails."killData"->'victim'->'shipType'->>'id')::int as typeID,
      "invTypes"."typeName",
      "mapSolarSystems"."solarSystemName",
      "mapSolarSystems"."security"
    FROM
      data.killmails,
      public."invTypes",
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      (killmails."killData"->'victim'->'shipType'->>'id')::int = "invTypes"."typeID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapSolarSystems"."solarSystemID" = (killmails."killData"->'solarSystem'->>'id')::int AND
      public."mapSolarSystems"."regionID" = %s AND
      (killmails."killData"->'victim'->'shipType'->>'id')::int NOT IN (33477)
    ORDER BY
     timestamp DESC
    LIMIT 100
    '''
    data = (regionID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp','killID','killHash','totalValue','attackerCount','damageTaken','allianceName', 'typeID', 'typeName', 'solarSystemName', 'security'])
    cursor.close()
    df['timestamp'] = df['timestamp'].str.replace('.','-')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df.reset_index().to_json(orient='records',date_format='iso')


#############################
# moonReport
#############################

def getmoonmineralsbyregion(regionID):  # TODO change join to return results when no sov exists
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
      meta.alliances,
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
    cursor.close()
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
      sov."allianceID",
      alliances.name,
      alliances.ticker
    FROM
      data.moonminerals,
      public."mapDenormalize",
      public."invTypes",
      public."mapSolarSystems",
      public."mapRegions",
      meta.alliances,
      map.sov
    WHERE
      "mapDenormalize"."itemID" = moonminerals."moonID" AND
      "invTypes"."typeID" = moonminerals."typeID" AND
      "mapSolarSystems"."solarSystemID" = "mapDenormalize"."solarSystemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      alliances."allianceID" = sov."allianceID" AND
      sov."solarSystemID" = "mapDenormalize"."solarSystemID" AND
      "invTypes"."typeID" = %s
    '''
    data = (typeID, )
    cursor.execute(sql, data, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    cursor.close()
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
      meta.alliances,
      map.sov
    WHERE
      "mapDenormalize"."itemID" = moonminerals."moonID" AND
      "invTypes"."typeID" = moonminerals."typeID" AND
      "mapSolarSystems"."solarSystemID" = "mapDenormalize"."solarSystemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      alliances."allianceID" = sov."allianceID" AND
      sov."solarSystemID" = "mapDenormalize"."solarSystemID" AND
      "invTypes"."typeID" = %s
    GROUP BY
      alliances.name,
      alliances.ticker
    ORDER BY
      SUM_moonID DESC'''
    data = (typeID, )
    cursor.execute(sql, data, )
    cursor.close()
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
      meta.alliances,
      map.sov
    WHERE
      "mapDenormalize"."itemID" = moonminerals."moonID" AND
      "invTypes"."typeID" = moonminerals."typeID" AND
      "mapSolarSystems"."solarSystemID" = "mapDenormalize"."solarSystemID" AND
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      alliances."allianceID" = sov."allianceID" AND
      sov."solarSystemID" = "mapDenormalize"."solarSystemID"
    GROUP BY
      alliances.name,
      alliances.ticker
    ORDER BY
      SUM_moonID DESC'''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    cursor.close()
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def getdeadendsystems(gateCountLimit):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      COUNT("mapSolarSystemJumps"."fromSolarSystemID") as gateCount,
      COUNT("conquerablestations"."name") as stationCount,
      "mapSolarSystems"."solarSystemID",
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName",
      alliances."allianceID",
      alliances.ticker,
      alliances.name
    FROM
      public."mapSolarSystemJumps",
      public."mapSolarSystems",
      public."mapRegions",
      data.mapsov,
      meta.alliances,
      data.conquerablestations
    WHERE
      "mapSolarSystemJumps"."toSolarSystemID" = "mapSolarSystems"."solarSystemID" AND
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      mapsov."solarSystemID" = "mapSolarSystems"."solarSystemID" AND
      alliances."allianceID" = mapsov."allianceID" AND
      conquerablestations."solarSystemID" = "mapSolarSystems"."solarSystemID"
    GROUP BY
      "mapSolarSystems"."solarSystemID",
      "mapSolarSystems"."solarSystemName",
      "mapRegions"."regionName",
      alliances."allianceID",
      alliances.ticker,
      alliances.name
    HAVING COUNT("mapSolarSystemJumps"."fromSolarSystemID") = %s'''
    data = (gateCountLimit, )
    cursor.execute(sql, data, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    cursor.close()
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


#############################
# Map
#############################

def mapjumps_solarsystemID(solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      timestamp,
      mapjumps."shipJumps",
      "mapSolarSystems"."solarSystemName"
    FROM
      data.mapjumps,
      public."mapSolarSystems"
    WHERE mapjumps."solarSystemID" = %s AND
      "mapSolarSystems"."solarSystemID" = mapjumps."solarSystemID" AND
      timestamp < TIMESTAMP 'yesterday'
    ORDER BY mapjumps."timestamp" DESC'''
    data = (solarSystemID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp','shipJumps','solarSystemName'])
    cursor.close()
    df = pd.pivot_table(df,index='timestamp',columns='solarSystemName',values='shipJumps')
    df = df.resample("12H",how='sum')
    return df.reset_index().to_json(orient='records',date_format='iso')


def mapjumps_tradehubs():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      timestamp,
      mapjumps."shipJumps",
      "mapSolarSystems"."solarSystemName"
    FROM
      data.mapjumps,
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."solarSystemID" = mapjumps."solarSystemID" AND
      mapjumps."solarSystemID" IN (30002187, 30000142, 30002659, 30002510) AND
      timestamp < TIMESTAMP 'yesterday'
    ORDER BY mapjumps."timestamp" DESC'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp','shipJumps','solarSystemName'])
    cursor.close()
    df = pd.pivot_table(df,index='timestamp',columns='solarSystemName',values='shipJumps')
    df = df.resample("12H",how='sum')
    return df.reset_index().to_json(orient='records',date_format='iso')


def mapkills_jumpsbyregion(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mapjumps."timestamp",
      SUM(mapjumps."shipJumps") as SUM_shipJumps,
      "mapRegions"."regionName"
    FROM
      data.mapjumps,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."solarSystemID" = mapjumps."solarSystemID" AND
      "mapSolarSystems"."regionID" = %s AND
      timestamp < TIMESTAMP 'yesterday'
    GROUP BY
      mapjumps."timestamp",
      "mapRegions"."regionName"
    ORDER BY mapjumps."timestamp" DESC
      '''
    data = (regionID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp','SUM_shipJumps','regionName'])
    cursor.close()
    df = pd.pivot_table(df,index='timestamp',columns='regionName',values='SUM_shipJumps')
    df = df.resample("12H",how='sum')
    return df.reset_index().to_json(orient='records',date_format='iso')


def mapkills_npckillsbyregion(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      kill."timestamp",
      SUM(kill."factionKills") as SUM_factionKills,
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."solarSystemID" = kill."solarSystemID" AND
      "mapSolarSystems"."regionID" = %s AND
      timestamp < TIMESTAMP 'yesterday'
    GROUP BY
      kill."timestamp",
      "mapRegions"."regionName"
    ORDER BY kill."timestamp" DESC
      '''
    data = (regionID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp','SUM_factionKills','regionName'])
    cursor.close()
    df = pd.pivot_table(df,index='timestamp',columns='regionName',values='SUM_factionKills')
    df = df.resample("12H",how='sum')
    return df.reset_index().to_json(orient='records',date_format='iso')


def mapkills_shipkillsbyregion(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      kill."timestamp",
      SUM(kill."shipKills") as SUM_shipKills,
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."solarSystemID" = kill."solarSystemID" AND
      "mapSolarSystems"."regionID" = %s AND
      timestamp < TIMESTAMP 'yesterday'
    GROUP BY
      kill."timestamp",
      "mapRegions"."regionName"
    ORDER BY kill."timestamp" DESC
      '''
    data = (regionID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp','SUM_shipKills','regionName'])
    cursor.close()
    df = pd.pivot_table(df,index='timestamp',columns='regionName',values='SUM_shipKills')
    df = df.resample("12H",how='sum')
    return df.reset_index().to_json(orient='records',date_format='iso')


def mapkills_podkillsbyregion(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      kill."timestamp",
      SUM(kill."podKills") as SUM_podKills,
      "mapRegions"."regionName"
    FROM
      map.kill,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."solarSystemID" = kill."solarSystemID" AND
      "mapSolarSystems"."regionID" = %s AND
      timestamp < TIMESTAMP 'yesterday'
    GROUP BY
      kill."timestamp",
      "mapRegions"."regionName"
    ORDER BY kill."timestamp" DESC
      '''
    data = (regionID, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['timestamp','SUM_podKills','regionName'])
    cursor.close()
    df = pd.pivot_table(df,index='timestamp',columns='regionName',values='SUM_podKills')
    df = df.resample("12H",how='sum')
    return df.reset_index().to_json(orient='records',date_format='iso')


#############################
# Process - Update Moons
#############################

def getverifiedmoonscrest():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT "moonID", "typeID" FROM data."moonverify"'''
    cursor.execute(sql, )
    result = cursor.fetchall()
    return result


def getverifiedmoonsevemoons():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT "moonID", "typeID" FROM data."moonevemoons"'''
    cursor.execute(sql, )
    result = cursor.fetchall()
    return result


def updatemoonmineralstable(moonID, typeID):
    insertcount = 0
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        sql = 'INSERT INTO data."moonminerals" ("moonID", "typeID") VALUES (%s, %s)'
        data = (moonID, typeID, )
        cursor.execute(sql, data, )
    except psycopg2.IntegrityError:
        conn.rollback()
    else:
        conn.commit()
        insertcount += 1
    return insertcount

#############################
# indexReports
#############################

def getindextypeids(typeIDlist, divisor):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
          (history.volume * history."avgPrice" * history."orderCount") / %s AS index,
          history."timestamp"
        FROM
          market.history
        WHERE
          history."typeID" IN %s
        GROUP BY index, history."timestamp"
        ORDER BY history."timestamp" ASC'''
    data = (divisor, typeIDlist, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['index','timestamp'])
    cursor.close()
    df = df.groupby(['timestamp']).mean()
    df = df.resample("1W")
    return df.reset_index().to_json(orient='records',date_format='iso')


def getkillmails_typeid_solarsystem(typeIDs, solarSystemIDs):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
     COUNT(kill.mail."killData"->'solarSystem'->'id') as count,
     kill.mail."killData"->'killTime' as timestamp
    FROM
     kill.mail
    WHERE
     (kill.mail."killData"->'victim'->'shipType'->>'id')::int IN %s AND
     (kill.mail."killData"->'solarSystem'->>'id')::int IN %s
    GROUP BY
     timestamp
    ORDER BY
     timestamp DESC'''
    data = (typeIDs, solarSystemIDs, )
    cursor.execute(sql, data, )
    df = pd.DataFrame(cursor.fetchall(),columns=['count','timestamp'])
    cursor.close()
    df['timestamp'] = df['timestamp'].str.replace('.','-')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    df = df.resample("1M",how='sum')
    return df.reset_index().to_json(orient='records',date_format='iso')
