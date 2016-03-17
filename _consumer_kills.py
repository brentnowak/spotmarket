from _utility import *

def getclosestmoon(solarSystemID, x, y, z):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      "mapDenormalize"."solarSystemID",
      ABS(%s - "mapDenormalize".x) +
      ABS(%s - "mapDenormalize".y) +
      ABS(%s - "mapDenormalize".z) as totalDiff,
      "mapDenormalize"."itemName",
      "mapDenormalize"."itemID"
    FROM
      public."mapDenormalize"
    WHERE "mapDenormalize"."solarSystemID" = %s AND
    "mapDenormalize"."typeID" = 14
    ORDER BY totalDiff ASC
    LIMIT 1'''
    data = (x, y, z, solarSystemID, )
    cursor.execute(sql, data, )
    results = cursor.fetchone()
    cursor.close()
    return results


def insertmoonverifyrecord(moonID, killID, typeID):
    insertcount = 0
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        sql = 'INSERT INTO data."moonverify" ("moonID", "killID", "typeID") VALUES (%s, %s, %s)'
        data = (moonID, killID, typeID, )
        cursor.execute(sql, data, )
    except psycopg2.IntegrityError:
        conn.rollback()
    else:
        conn.commit()
        insertcount += 1
    return insertcount


def insertmoonrecordverifygroup(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      "invTypes"."marketGroupID"
    FROM
      public."invTypes"
    WHERE "invTypes"."typeID" = %s'''
    data = (typeID, )
    cursor.execute(sql, data, )
    result = cursor.fetchone()
    return result[0]


def insertkillmailrecord(killID, killHash, killData, totalValue):
    insertcount = 0
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
          killmails."killID",
          killmails."killHash",
          killmails."killData"
        FROM
          data.killmails
        WHERE killmails."killID" = %s AND
        killmails."killHash" = %s'''
    data = (killID, killHash, )
    cursor.execute(sql, data, )
    results = cursor.fetchone()

    if results == None:  # No killmail, insert all records
        try:
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            sql = '''INSERT INTO data."killmails"
                ("killID", "killHash", "killData", "totalValue")
                VALUES (%s, %s, %s, %s)'''
            data = (killID, killHash, killData, totalValue, )
            cursor.execute(sql, data, )
        except psycopg2.IntegrityError:
            conn.rollback()
        else:
            conn.commit()
            insertcount += 1
        return insertcount

    if results[2] == None:  # killmail without json record, insert json
        try:
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            sql = '''UPDATE
                data."killmails"
                SET "killData" = %s
                WHERE killmails."killID" = %s AND
                killmails."killHash" = %s'''
            data = (killData, killID, killHash)
            cursor.execute(sql, data, )
        except psycopg2.IntegrityError:
            conn.rollback()
        else:
            conn.commit()
    conn.close()
    return 0  # killmail exists, return insertCount 0


def getzkbships():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      killmailsitems."typeID"
    FROM
      data.killmailsitems
     WHERE killmailsitems.enabled = 1'''
    cursor.execute(sql, )
    result = cursor.fetchall()
    return result


def getzkbpagenumber(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      killmailsitems."lastPage"
    FROM
      data.killmailsitems
     WHERE killmailsitems."typeID" = %s'''
    data = (typeID, )
    cursor.execute(sql, data, )
    result = cursor.fetchone()
    return result


def setzkbshipenable(typeID, enabled):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''UPDATE data.killmailsitems
        SET enabled = %s
        WHERE killmailsitems."typeID" = %s'''
    data = (enabled, typeID, )
    cursor.execute(sql, data, )
    conn.commit()
    conn.close()
    return 0


def setzkbshipresult(typeID, importResult):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''UPDATE data.killmailsitems
        SET "importResult" = %s
        WHERE killmailsitems."typeID" = %s'''
    data = (importResult, typeID, )
    cursor.execute(sql, data, )
    conn.commit()
    conn.close()
    return 0


# Input
# Output    1 for existing killmail
#           0 for no killmail
def checkforkillmail(killID, killHash):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      COUNT(killmails."killData")
    FROM
      data.killmails
    WHERE killmails."killID" = %s AND
      killmails."killHash" = %s'''
    data = (killID, killHash, )
    cursor.execute(sql, data, )
    result = cursor.fetchone()
    if result[0] == 1:
        return True
    else:
       return False


def setzkblastpage(typeID, lastPage):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''UPDATE data.killmailsitems
        SET "lastPage" = %s
        WHERE killmailsitems."typeID" = %s'''
    data = (lastPage, typeID)
    cursor.execute(sql, data, )
    conn.commit()
    conn.close()
    return 0
