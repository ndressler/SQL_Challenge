import sqlite3


conn = sqlite3.connect('cocktails_database.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT * FROM glas")
c.fetchall()
