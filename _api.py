from _utility import *

def getcharacterblueprints():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = '''SELECT
      characters."characterName",
      "invTypes"."typeName",
      "invTypes"."typeID",
      charblueprints.quantity,
      charblueprints.timeefficiency,
      charblueprints.materialefficiency,
      charblueprints.runs
    FROM
      data.charblueprints,
      data.characters,
      public."invTypes"
    WHERE
      charblueprints."characterID" = characters."characterID" AND
      "invTypes"."typeID" = charblueprints."typeID" AND
      characters."characterID" = charblueprints."characterID"'''
    cursor.execute(sql, )
    results = json.dumps(cursor.fetchall(), indent=2, default=date_handler)
    cursor.close()
    if len(results) < 1:     # Handle a empty table
        return "No Data"
    else:
        return results
