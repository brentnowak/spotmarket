from _utility import *

def getdbtablesizes():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT relname AS "element",
      pg_size_pretty(pg_total_relation_size(C.oid)) AS "totalSize"
    FROM pg_class C
    LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
    WHERE nspname NOT IN ('pg_catalog', 'information_schema')
    AND C.relkind <> 'i'
    AND nspname !~ '^pg_toast'
    ORDER BY pg_total_relation_size(C.oid) DESC
    LIMIT 10'''
    cursor.execute(sql, )
    df = pd.DataFrame(cursor.fetchall())
    cursor.close()
    return df.reset_index().to_json(orient='records', date_format='iso')


def getdbsize():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT pg_size_pretty(pg_database_size('spotmarket'))'''
    cursor.execute(sql, )
    result = cursor.fetchone()
    return result
