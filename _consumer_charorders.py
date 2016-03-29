from _utility import *


def trunkcharorders():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''TRUNCATE  data."charorders"'''
    cursor.execute(sql, )
    conn.commit()
    conn.close()
    return 0


def insertorders(characterID, orderID, stationID, volEntered, volRemaining, orderState, typeID, range, accountKey, duration, escrow, price, bid, issued):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''INSERT INTO data."charorders"
        (characterID,
            orderID,
            stationID,
            volEntered,
            volRemaining,
            orderState,
            typeID,
            range,
            accountKey,
            duration,
            escrow,
            price,
            bid,
            issued)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s  %s, %s, %s, %s)'''
    data = (characterID, orderID, stationID, volEntered, volRemaining, orderState, typeID, range, accountKey, duration, escrow, price, bid, issued, )
    cursor.execute(sql, data)
    conn.commit()
    conn.close()
    return 0
