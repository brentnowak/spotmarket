from _utility import *

#
# Input         alliance_data
# Output        'alliances' Database insert
#
def insertalliancesrecords(alliance_data):
    insertcount = 0
    for key,value in alliance_data.iteritems():
        try:
            allianceID = value['id']
            ticker = value['ticker']
            name = value['name']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            sql = 'INSERT INTO meta."alliances" ("allianceID", "ticker", "name") VALUES (%s, %s, %s)'
            data = (allianceID, ticker, name, )
            cursor.execute(sql, data, )
        except psycopg2.IntegrityError:
            conn.rollback()
        else:
            conn.commit()
            insertcount += 1
    return insertcount
