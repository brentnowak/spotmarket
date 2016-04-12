from _utility import *

#
# Input         alliance_data
# Output        'alliance' Database insert
#
def alliance_insertrecords(alliance_data):
    insertcount = 0
    for key,value in alliance_data.iteritems():
        try:
            allianceID = value['id']
            ticker = value['ticker']
            name = value['name']
            executorCorpID = value['executor_id']
            memberCount = value['member_count']
            startDate = value['timestamp']
            startDate = arrow.get(startDate)
            startDate = startDate.format('YYYY-MM-DD HH:mm:ss')
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            sql = 'INSERT INTO meta.alliance ("allianceID", "ticker", "name", "executorCorpID", "memberCount", "startDate") VALUES (%s, %s, %s, %s, %s, %s)'
            data = (allianceID, ticker, name, executorCorpID, memberCount, startDate, )
            cursor.execute(sql, data, )
        except psycopg2.IntegrityError:
            conn.rollback()
        else:
            conn.commit()
            insertcount += 1
    return insertcount
