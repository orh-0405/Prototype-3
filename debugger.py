import sqlite3
#use this to try and fix the problem of OperationalError: unable to open database file
db = sqlite3.connect("chat_with_profdb/Profx.db")
db.close()
