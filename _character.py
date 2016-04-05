from _utility import *


def character_trunkskillqueue():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''TRUNCATE  "character".skillqueue'''
    cursor.execute(sql, )
    conn.commit()
    conn.close()
    return 0


def character_insertskillqueue(characterID, endTime, level, typeID, startTime, endSP, startSP, queuePosition):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''INSERT INTO "character".skillqueue
        ("characterID",
            "endTime",
            level,
            "typeID",
            "startTime",
            "endSP",
            "startSP",
            "queuePosition")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    data = (characterID, endTime, level, typeID, startTime, endSP, startSP, queuePosition, )
    cursor.execute(sql, data)
    conn.commit()
    conn.close()
    return 0
