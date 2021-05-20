import os.path, sqlite3
from sqlite3 import Error
import datetime

def get_db(Dbname):
    
    db = sqlite3.connect(Dbname, check_same_thread= False)
    print("Opened database successfully")
    db.row_factory = sqlite3.Row
    return(db)

def create_table(table_name, db_name):
    curr_dir = os.path.dirname(__file__)
    db_file_name = os.path.join(curr_dir, "{}.db".format(db_name))
    db = get_db(db_name)
    query = '''
    CREATE TABLE {}
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    message TEXT)
    '''.format(table_name)
    db.execute(query)
    print("Table created successfully")
    db.close()

def checkpassword(username, password):
    #db = get_db("Users.db")
    db = sqlite3.connect("Users.db")
    query = "SELECT Password FROM User WHERE Name = 'A'"
    try:
        print("I")
        cursor = db.execute(query)
        print("#")
        data = cursor.fetchone()
    except Error as e:
        db.close()
        return(e)
    if data == None:
        db.close()
        return("UNF")
    if password == data[0]:
        query = "UPDATE main.User SET Login = 1 WHERE Name  = ?"
        db.execute(query, (username,))
        db.commit()
        db.close()
        return("S")
        
    else:
        db.close()
        return("PC")
        

def get_account_type():
    db = get_db("Users.db")
    query = "SELECT acc FROM User WHERE Login = 1"
    try:
        cursor = db.execute(query)
        data = cursor.fetchone()
    except Error as e:
        return(e)
    if data == None:
        return("DLI")
    else:
        return(data["acc"])
    db.close()


def get_user():
    db = get_db("Users.db")
    query = "SELECT Name FROM Users WHERE Login = 1"
    try:
        cursor = db.execute(query)
        data = cursor.fetchone()
    except Error as e:
        db.close()
        return(e)
    if data == None:
        db.close()
        return("DLI")
    else:
        db.close()
        return(data["Name"])

def list_of_prof():
    db = get_db("Users.db")
    query = "SELECT Name FROM User WHERE acc = 'prof'"
    
    data = []
    cursor = db.execute(query)
    temp = cursor.fetchall()
    for i in temp:
        data.append(i["Name"])
    db.close()
    return(data)

def list_of_stu():
    db = get_db("Users.db")
    query = "SELECT Name FROM User WHERE acc = 'stu'"
    
    data = []
    cursor = db.execute(query)
    temp = cursor.fetchall()
    for i in temp:
        data.append(i["Name"])
    db.close()
    return(data)

def new(name, message):
    db = get_db()
    user = get_user()
    query = "INSERT INTO {} (Name, Message, Time) VALUES(?,?,?)".format("Chat" + user)
    now = datetime.now()  #gets current time
    current_time = now.strftime("%H:%M")
    db.execute(query, (name, message, current_time))

    db.commit()
    db.close()
#if not os.path.isfile("chat_with_prof.db"):
#    create_db(db_file_name)