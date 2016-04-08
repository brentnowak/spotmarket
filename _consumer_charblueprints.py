from _utility import *


def trunkcharblueprints():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''TRUNCATE "character".blueprint'''
    cursor.execute(sql, )
    conn.commit()
    conn.close()
    return 0


def insertblueprintsitems(characterID, itemID, locationID, typeID, quantity, flagID, timeEfficiency, materialEfficiency, runs):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''INSERT INTO "character".blueprint
        ("characterID",
            "itemID",
            "locationID",
            "typeID",
            quantity,
            "flagID",
            "timeEfficiency",
            "materialEfficiency",
            runs)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    data = (characterID, itemID, locationID, typeID, quantity, flagID, timeEfficiency, materialEfficiency, runs, )
    cursor.execute(sql, data)
    conn.commit()
    conn.close()
    return 0
