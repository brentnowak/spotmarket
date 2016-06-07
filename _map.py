from _utility import *

#
# Usage         consumer_map.py
# Input         mapapi_data, maptimestamp
# Output        'mapkills' Database insert
#
def map_insertkillsrecords(killsapi_data, maptimestamp):
    insertcount = 0
    for key,value in killsapi_data.iteritems():
        try:
            id = value['id']
            ship = value['ship']
            faction = value['faction']
            pod = value['pod']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            sql = 'INSERT INTO map.kill (timestamp, "solarSystemID", "shipKills", "factionKills", "podKills") VALUES (%s, %s, %s, %s, %s)'
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
def map_insertjumpsrecords(jumps_data, jumpstimestamp):
    insertcount = 0
    for key,value in jumps_data.iteritems():
        try:
            id = key
            jumps = value
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            sql = 'INSERT INTO map.jump (timestamp, "solarSystemID", "shipJumps") VALUES (%s, %s, %s)'
            data = (jumpstimestamp, id, jumps, )
            cursor.execute(sql, data, )
        except psycopg2.IntegrityError:
            conn.rollback()
        else:
            conn.commit()
            insertcount += 1
    return insertcount


#
# Insert sov data if solarSystemID doesn't have the same corporationID
#
def map_insertsov(sovapi_data, sovtimestamp):
    count_insert = 0
    for key,value in sovapi_data.iteritems():
        solarSystemID = value['id']
        allianceID = value['alliance_id']
        corporationID = value['corp_id']
        factionID = value['faction_id'] # Not used
        solarSystemName = value['name'] # Not used
        if str(allianceID) != "None":   # Filter out factions
            if getmaptopsov(solarSystemID) != corporationID:
                map_insertmapsovrecord(sovtimestamp, allianceID, corporationID, solarSystemID)
                count_insert += 1
    return count_insert


#
# Get latest sov record
#
def getmaptopsov(solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      sov."corporationID"
    FROM
      map.sov
    WHERE sov."solarSystemID" = %s
    ORDER BY sov."timestamp" DESC
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
# Insert latest sov record because corporationID has changed for solarSystemID
#
def map_insertmapsovrecord(timestamp, allianceID, corporationID, solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = 'INSERT INTO map.sov (timestamp, "allianceID", "corporationID", "solarSystemID") VALUES (%s, %s, %s, %s)'
    data = (timestamp, allianceID, corporationID, solarSystemID, )
    cursor.execute(sql, data)
    conn.commit()
    conn.close()
    return 0


def mapjumps_solarsystemID(solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      timestamp,
      jump."shipJumps",
      "mapSolarSystems"."solarSystemName"
    FROM
      map.jump,
      public."mapSolarSystems"
    WHERE jump."solarSystemID" = %s AND
      "mapSolarSystems"."solarSystemID" = jump."solarSystemID" AND
      timestamp < TIMESTAMP 'yesterday'
    ORDER BY jump."timestamp" DESC'''
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
      jump."shipJumps",
      "mapSolarSystems"."solarSystemName"
    FROM
      map.jump,
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."solarSystemID" = jump."solarSystemID" AND
      jump."solarSystemID" IN (30002187, 30000142, 30002659, 30002510) AND
      timestamp < TIMESTAMP 'yesterday'
    ORDER BY jump."timestamp" DESC'''
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
      jump."timestamp",
      SUM(jump."shipJumps") as SUM_shipJumps,
      "mapRegions"."regionName"
    FROM
      map.jump,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapSolarSystems"."regionID" = "mapRegions"."regionID" AND
      "mapSolarSystems"."solarSystemID" = jump."solarSystemID" AND
      "mapSolarSystems"."regionID" = %s AND
      timestamp < TIMESTAMP 'yesterday'
    GROUP BY
      jump."timestamp",
      "mapRegions"."regionName"
    ORDER BY jump."timestamp" DESC
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
    SUM(jump."shipJumps") as shipJumps,
      jump."timestamp"
    FROM
      map.jump,
      public."mapRegions",
      public."mapSolarSystems"
    WHERE
      "mapRegions"."regionID" = "mapSolarSystems"."regionID" AND
      "mapSolarSystems"."solarSystemID" = jump."solarSystemID" AND
      public."mapSolarSystems"."regionID" IN %s AND
      timestamp < TIMESTAMP 'yesterday'
    GROUP BY jump."timestamp"
    ORDER BY timestamp DESC
    '''
    data = (regions, )
    cursor.execute(sql, data)
    df = pd.DataFrame(cursor.fetchall(),columns=[regionName, 'timestamp'])
    df = df.set_index(['timestamp'])
    df = df.resample("12H",how='sum')
    cursor.close()
    return df.reset_index().to_json(orient='records', date_format='iso')


def map_solarsystems_region(regionID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    sql = '''
    SELECT "solarSystemName" as "name",
    "solarSystemID"
    FROM public."mapSolarSystems"
    WHERE "regionID" = %s
    '''
    data = (regionID, )
    cursor.execute(sql, data, )
    results = cursor.fetchall()
    return results


def map_solarsystem_connections(solarSystemID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''
    SELECT "toSolarSystemID"
    FROM public."mapSolarSystemJumps"
    WHERE "fromSolarSystemID" = %s
    '''
    data = (solarSystemID,)
    cursor.execute(sql, data, )
    results = cursor.fetchall()
    return results

