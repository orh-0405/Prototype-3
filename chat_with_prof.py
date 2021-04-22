import os.path, sqlite3

def get_db():
    db = sqlite3.connect(db_file_name, check_same_thread= False)
    print("Opened database successfully")
    db.row_factory = sqlite3.Row
    return(db)

def create_db(db_file_name):
    db = get_db()
    query = '''
    CREATE TABLE posting
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    message TEXT)
    '''
    db.execute(query)
    print("Table created successfully")
    db.close()

curr_dir = os.path.dirname(__file__)
db_file_name = os.path.join(curr_dir, "chat_with_prof.db")

if not os.path.isfile("chat_with_prof.db"):
    create_db(db_file_name)