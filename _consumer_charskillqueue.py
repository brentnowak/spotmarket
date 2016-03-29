from _utility import *


def trunkcharskillqueue():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''TRUNCATE  data."charskillqueues"'''
    cursor.execute(sql, )
    conn.commit()
    conn.close()
    return 0


def insertskillqueueitems(characterID, endTime, level, typeID, startTime, endSP, startSP, queuePosition):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''INSERT INTO data."charskillqueues"
        ("characterID",
            endtime,
            level,
            "typeID",
            starttime,
            endsp,
            startsp,
            queueposition)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    data = (characterID, endTime, level, typeID, startTime, endSP, startSP, queuePosition, )
    cursor.execute(sql, data)
    conn.commit()
    conn.close()
    return 0
