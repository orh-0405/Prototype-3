import sqlite3
db ="Profx.db"
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
query = "SELECT * FROM ChatA"
cursor = conn.execute(query)
data = cursor.fetchall()
conn.close()
print(data["Name"])