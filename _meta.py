from _utility import *

def meta_insertconquerablestation(station_data):
    insertcount = 0
    for key,value in station_data.iteritems():
        try:
            solarSystemID = value['system_id']
            stationID = value['id']
            x = value['x']
            y = value['y']
            z = value['z']
            name = value['name']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            sql = 'INSERT INTO meta.conquerablestation ("solarSystemID", "stationID", "x", "y", "z", "name") VALUES (%s, %s, %s, %s, %s, %s)'
            data = (solarSystemID, stationID, x, y, z, name)
            cursor.execute(sql, data, )
        except psycopg2.IntegrityError:
            conn.rollback()
        else:
            conn.commit()
            insertcount += 1
    return insertcount


def coalition_insertcollation(coalitionID, coalitionName):
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        sql = 'INSERT INTO meta."coalition" ("coalitionID", "name") VALUES (%s, %s)'
        data = (coalitionID, coalitionName, )
        cursor.execute(sql, data, )
    except psycopg2.IntegrityError:
        conn.rollback()
    else:
        conn.commit()
    return 0


def collation_updatecoalition(coalitionID, allianceID):
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        sql = '''UPDATE meta.alliance
            SET "coalitionID" = %s
            WHERE "allianceID" = %s'''
        data = (coalitionID, allianceID, )
        cursor.execute(sql, data, )
    except psycopg2.IntegrityError:
        conn.rollback()
    else:
        conn.commit()
    return 0
