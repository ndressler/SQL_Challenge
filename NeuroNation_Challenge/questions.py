import sqlite3


conn = sqlite3.connect('cocktails_database.sqlite')
conn.row_factory = sqlite3.Row
db = conn.cursor()
query = """SELECT gname
    FROM glas
    ORDER BY gname ASC
    """
results = db.fetchall()
print(results)
