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
    results = cursor.fetchall()
    return results


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
    if result[0] == None: #  If no entry for lastPage in table, return 1
        return 1
    else:
        return result[0]


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
    data = (lastPage, typeID, )
    cursor.execute(sql, data, )
    conn.commit()
    conn.close()
    return 0


def getkmemptyvalue():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      killmails."killID",
      killmails."killHash"
    FROM
      data.killmails
    WHERE killmails."totalValue" IS NULL
    LIMIT 1'''
    cursor.execute(sql, )
    return cursor.fetchone()


def getkmemptyjson():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      killmails."killID",
      killmails."killHash"
    FROM
      data.killmails
    WHERE killmails."killData" IS NULL
    LIMIT 1'''
    cursor.execute(sql, )
    return cursor.fetchone()


def gettotalkmemptyvalues():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      COUNT(*)
    FROM
      data.killmails
    WHERE killmails."totalValue" IS NULL'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]


def setkmtotalvalue(killID, totalValue):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''UPDATE data.killmails
        SET "totalValue" = %s
        WHERE killmails."killID" = %s'''
    data = (totalValue, killID, )
    cursor.execute(sql, data, )
    conn.commit()
    conn.close()
    return 0


def getminkmid():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      MIN(killmails."killmailID")
    FROM
      data.killmails'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]


def getmaxkmid():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      MAX(killmails."killmailID")
    FROM
      data.killmails'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]

def getkillid(killmailID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      killmails."killID"
    FROM
      data.killmails
    WHERE "killmailID" = %s'''
    data = (killmailID, )
    cursor.execute(sql, data, )
    result = cursor.fetchone()
    if result != None:
        return result[0]
    else:
        return 0


def getkmdetails(killID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''
    SELECT
      killmails."killmailID",
      killmails."killID",
      (killmails."killData"->'victim'->'shipType'->'id')::text::int as typeID,
      (killmails."killData"->'victim'->'character'->'id')::text::int as characterID,
      (killmails."killData"->'victim'->'corporation'->'id')::text::int as corporationID,
      (killmails."killData"->'solarSystem'->'id')::text::int as solarSystemID,
      (killmails."killData"->'attackerCount')::text::int as attackerCount,
      (killmails."killData"->'victim'->'damageTaken')::text::int as damageTaken,
      (killmails."killData"->'killTime')::text as timestamp,
      (killmails."killData"->'victim'->'position'->'x')::text::real as x,
      (killmails."killData"->'victim'->'position'->'y')::text::real as y,
      (killmails."killData"->'victim'->'position'->'z')::text::real as z,
      killmails."totalValue"
    FROM
      data.killmails
    WHERE killmails."killID" = %s
    '''
    data = (killID, )
    cursor.execute(sql, data, )
    results = cursor.fetchone()
    return results

def insertkillmailsumrecord(killID, characterID, corporationID, typeID, attackerCount, damageTaken, timestamp, solarSystemID, x, y, z):
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        sql = '''INSERT INTO data.killmailssum(
          "killID", "characterID", "corporationID", "typeID",
          "attackerCount", "damageTaken", "timestamp", "solarSystemID", x, y, z)
        VALUES
          (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        data = (killID, characterID, corporationID, typeID, attackerCount, damageTaken, timestamp, solarSystemID, x, y, z, )
        cursor.execute(sql, data, )
    except psycopg2.IntegrityError:
        conn.rollback()
    else:
        conn.commit()
    return 0

