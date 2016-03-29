from _utility import *


def getwallettransactions():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      to_char(charwallet."transactionDateTime", 'YYYY-MM-dd HH:mm:ss') AS transactionDateTime,
      charwallet."transactionID",
      charwallet."typeID",
      charwallet."typeName",
      charwallet.quantity,
      charwallet.price,
      charwallet."clientName",
      charwallet."stationID",
      charwallet."stationName",
      charwallet."transactionType",
      charwallet.personal,
      charwallet.profit
    FROM
      data.charwallet
    ORDER BY charwallet."transactionDateTime" DESC
    '''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def insertwallettransaction(transactionDateTime, transactionID, quantity, typeName, typeID, price, clientID, clientName, walletID, stationID, stationName, transactionType, personal, profit):
    insertcount = 0
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        sql = '''INSERT INTO data.charwallet(
            "transactionDateTime",
            "transactionID",
            quantity,
            "typeName",
            "typeID",
            price,
            "clientID",
            "clientName",
            "walletID",
            "stationID",
            "stationName",
            "transactionType",
            personal,
            profit)
        VALUES (to_timestamp(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        data = (transactionDateTime, transactionID, quantity, typeName, typeID, price, clientID, clientName, walletID, stationID, stationName, transactionType, personal, profit, )
        cursor.execute(sql, data)
    except psycopg2.IntegrityError:
        conn.rollback()
    else:
        conn.commit()
        insertcount += 1
    return insertcount