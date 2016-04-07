from _utility import *


def getwallettransactions():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      to_char(wallet."transactionDateTime", 'YYYY-MM-dd HH:mm:ss') AS transactionDateTime,
      wallet."transactionID",
      wallet."typeID",
      wallet."typeName",
      wallet.quantity,
      wallet.price,
      wallet."clientName",
      wallet."stationID",
      wallet."stationName",
      wallet."transactionType",
      wallet.personal,
      wallet.profit
    FROM
      "character".wallet
    ORDER BY wallet."transactionDateTime" DESC
    '''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results


def insertwallettransaction(transactionDateTime, transactionID, quantity,
                            typeName, typeID, price, clientID, clientName,
                            characterID, stationID, transactionType, personal,
                            profit, transactionFor, journalTransactionID):
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        sql = '''INSERT INTO "character".wallet(
            "transactionDateTime",
            "transactionID",
            quantity,
            "typeName",
            "typeID",
            price,
            "clientID",
            "clientName",
            "characterID",
            "stationID",
            "transactionType",
            personal,
            profit,
            "transactionFor",
            "journalTransactionID")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        data = (transactionDateTime, transactionID, quantity, typeName,
                typeID, price, clientID, clientName, characterID, stationID,
                transactionType, personal, profit,
                transactionFor, journalTransactionID, )
        print(data)
        cursor.execute(sql, data)
    except psycopg2.IntegrityError:
        conn.rollback()
    else:
        conn.commit()
        return 1
    return 0
