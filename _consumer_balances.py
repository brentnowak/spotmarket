from _utility import *


def insertwalletbalances(characterID, balance, timestamp):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''INSERT INTO data."charbalances"
        ("characterID",
            balance,
            "timestamp")
        VALUES (%s, %s, %s)'''
    data = (characterID, balance, timestamp)
    cursor.execute(sql, data)
    conn.commit()
    conn.close()
    return 0
