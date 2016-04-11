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
