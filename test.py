import sqlite3
import os
curr_dir = os.path.dirname(__file__)
db_file = os.path.join(curr_dir, "chat_with_profdb")
db = os.path.join(db_file, "Profx.db.db")
conn = sqlite3.connect(db)
conn.close()