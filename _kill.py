from requests.exceptions import ConnectionError, ChunkedEncodingError
from _utility import *
import requests.packages.urllib3
import requests
import sys

requests.packages.urllib3.disable_warnings()


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
          mail."killID",
          mail."killHash",
          mail."killData"
        FROM
          kill.mail
        WHERE mail."killID" = %s AND
        mail."killHash" = %s'''
    data = (killID, killHash, )
    cursor.execute(sql, data, )
    results = cursor.fetchone()

    if results == None:  # No killmail, insert all records
        try:
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            sql = '''INSERT INTO kill."mail"
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
                kill."mail"
                SET "killData" = %s
                WHERE mail."killID" = %s AND
                mail."killHash" = %s'''
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
      tracking."typeID"
    FROM
      kill."tracking"
     WHERE tracking.enabled = 1'''
    cursor.execute(sql, )
    results = cursor.fetchall()
    return results


def getzkbpagenumber(typeID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      tracking."lastPage"
    FROM
      kill.tracking
     WHERE tracking."typeID" = %s'''
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
    sql = '''UPDATE kill.tracking
        SET enabled = %s
        WHERE tracking."typeID" = %s'''
    data = (enabled, typeID, )
    cursor.execute(sql, data, )
    conn.commit()
    conn.close()
    return 0


def setzkbshipresult(typeID, importResult):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''UPDATE kill.tracking
        SET "importResult" = %s
        WHERE tracking."typeID" = %s'''
    data = (importResult, typeID, )
    cursor.execute(sql, data, )
    conn.commit()
    conn.close()
    return 0


# Input
# Output    1 for existing killmail
#           0 for no killmail
def checkforkillmail(killID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      COUNT(mail."killData")
    FROM
      kill.mail
    WHERE mail."killID" = %s'''
    data = (killID, )
    cursor.execute(sql, data, )
    result = cursor.fetchone()
    if result[0] == 1:
        return True
    else:
       return False


def setzkblastpage(typeID, lastPage):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''UPDATE kill.tracking
        SET "lastPage" = %s
        WHERE tracking."typeID" = %s'''
    data = (lastPage, typeID, )
    cursor.execute(sql, data, )
    conn.commit()
    conn.close()
    return 0


def getkmemptyvalue():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      mail."killID",
      mail."killHash"
    FROM
      kill.mail
    WHERE mail."totalValue" IS NULL
    LIMIT 1'''
    cursor.execute(sql, )
    return cursor.fetchone()


def getkmemptyjson():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      mail."killID",
      mail."killHash"
    FROM
      kill.mail
    WHERE mail."killData" IS NULL
    LIMIT 1'''
    cursor.execute(sql, )
    return cursor.fetchone()


def gettotalkmemptyvalues():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      COUNT(*)
    FROM
      kill.mail
    WHERE mail."totalValue" IS NULL'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]


def setkmtotalvalue(killID, totalValue):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''UPDATE kill.mail
        SET "totalValue" = %s
        WHERE mail."killID" = %s'''
    data = (totalValue, killID, )
    cursor.execute(sql, data, )
    conn.commit()
    conn.close()
    return 0


def getminkmid():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      MIN(mail."killmailID")
    FROM
      kill.mail'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]


def getmaxkmid():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      MAX(mail."killmailID")
    FROM
      kill.mail'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]

def getkillid(killmailID):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT
      mail."killID"
    FROM
      kill.mail
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
      mail."killmailID",
      mail."killID",
      (mail."killData"->'victim'->'shipType'->>'id')::int as typeID,
      (mail."killData"->'victim'->'character'->>'id')::int as characterID,
      (mail."killData"->'victim'->'corporation'->>'id')::int as corporationID,
      (mail."killData"->'solarSystem'->>'id')::int as solarSystemID,
      (mail."killData"->>'attackerCount')::int as attackerCount,
      (mail."killData"->'victim'->>'damageTaken')::int as damageTaken,
      (mail."killData"->>'killTime')::text as timestamp,
      (mail."killData"->'victim'->'position'->>'x')::real as x,
      (mail."killData"->'victim'->'position'->>'y')::real as y,
      (mail."killData"->'victim'->'position'->>'z')::real as z,
      mail."totalValue"
    FROM
      kill.mail
    WHERE mail."killID" = %s
    '''
    data = (killID, )
    cursor.execute(sql, data, )
    results = cursor.fetchone()
    return results


def gettotalbadjson():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''SELECT COUNT(*)
    FROM
      kill.mail
    WHERE (mail."killData"->'victim'->'shipType'->'id')::text::int IS NULL
    '''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result[0]


def getkmbadjson():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''
    SELECT "killID", "killHash"
    FROM
      kill.mail
    WHERE (mail."killData"->'victim'->'shipType'->'id')::text::int IS NULL
    LIMIT 1'''
    cursor.execute(sql, )
    results = cursor.fetchone()
    return results


def setkmjson(killID, killData):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = '''UPDATE kill.mail
    SET "killData" = %s
    WHERE mail."killID" = %s'''
    data = (killData, killID,)
    cursor.execute(sql, data, )
    conn.commit()
    conn.close()
    return 0


def kills_getcrestdata(typeID, pageNum, killID, killHash, killTime, solarSystemID, totalValue):
    if checkforkillmail(killID) == False:  # Check if killmail exists, if not, fetch from CREST
        crestURL = 'https://public-crest.eveonline.com/killmails/' + str(killID) + '/' + str(killHash) + '/'
        print("[" + str(gettypeName(typeID)) + "][page:" + str(pageNum) + "][killTime:" + str(killTime) + "][killID:" + str(
            killID) + "][solarSystemName:" + str(getSolarSystemName(solarSystemID)) + "]")  # Feedback
        sys.stdout.flush()
        try:
            crestKill = requests.get(crestURL)
        except (ConnectionError, ChunkedEncodingError) as e:
            print(e)
        else:
            insertkillmailrecord(killID, killHash, crestKill.text, totalValue)
    else:
        print("[" + str(gettypeName(typeID)) + "][skip][killID:" + str(killID) + "]")
        sys.stdout.flush()
    return 0
