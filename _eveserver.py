from _utility import *

def eveserver_insertstatus(timestamp, players, status):
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        sql = '''INSERT INTO meta.tranquility
              ("timestamp", "players", "status")
              VALUES (%s, %s, %s)'''
        data = (timestamp, players, status, )
        cursor.execute(sql, data, )
    except psycopg2.IntegrityError:
        conn.rollback()
    else:
        conn.commit()
    return 0
