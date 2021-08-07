import os.path, sqlite3
from sqlite3 import Error
from datetime import datetime
import socket
from flask import templating

curr_dir = os.path.dirname(__file__)
db_file = os.path.join(curr_dir, "chat_with_profdb")

def get_db(Dbname):
    db_file_name = os.path.join(db_file, "{}".format(Dbname))
    db = sqlite3.connect(db_file_name)#problem should be check_same_thread = False
    print("Opened database successfully")
    db.row_factory = sqlite3.Row
    return(db)

def create_table(table_name, db_name):
    db_file_name = os.path.join(db_file, "{}.db".format(db_name))
    db = get_db(db_file_name)
    query = '''
    CREATE TABLE {} (
    "ID"	INTEGER,
	"Name"	TEXT NOT NULL,
	"Message"	TEXT NOT NULL,
	"Time"	TEXT NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT)
    );
    '''.format(table_name)
    db.execute(query)
    db.commit()
    print("Table created successfully")
    db.close()

def checkpassword(username, password):
    db_file_name = os.path.join(db_file, "Users.db")
    db = get_db(db_file_name)
    account_exist(username)
    query = "SELECT Password FROM User WHERE Name = '{}'".format(username)
    cursor = db.execute(query)
    data = cursor.fetchone()
    print("J", data)

    if data == None:
        return ("UNF")
    print("chat with profs username&pw", username, password)
    if password == data[0]:
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ## printing the hostname and ip_address
        print(f"IP Address: {ip_address}")      
        query = "UPDATE main.User SET Login = ? WHERE Name  = ?"
        db.execute(query, (ip_address, username))
        db.commit()
        db.close()
        return("S")
        
    else:
        db.close()
        return("PC")
        

def get_account_type():
    db_file_name = os.path.join(db_file, "Users.db")
    db = get_db(db_file_name)
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    print(f"IP Address: {ip_address}")      
    query = "SELECT acc FROM User WHERE Login = ?"
    try:
        cursor = db.execute(query, (ip_address,))
        data = cursor.fetchone()
        db.close()
    except Error as e:
        db.close()
        return(e)
    if data == None:
        db.close()
        return("DLI")
    else:
        db.close()
        return(data["acc"])
    


def get_user():
    db_file_name = os.path.join(db_file, "Users.db")
    db = get_db(db_file_name)
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    print(f"IP Address: {ip_address}") 
    query = "SELECT Name FROM User WHERE Login = ?"
    try:
        cursor = db.execute(query, (ip_address,))
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
    db_file_name = os.path.join(db_file, "Users.db")
    db = get_db(db_file_name)
    query = "SELECT Name FROM User WHERE acc = 'prof'"
    
    data = []
    cursor = db.execute(query)
    temp = cursor.fetchall()
    for i in temp:
        data.append(i["Name"])
    db.close()
    return(data)

def list_of_stu():
    db_file_name = os.path.join(db_file, "Users.db")
    db = get_db(db_file_name)
    query = "SELECT Name FROM User WHERE acc = 'stu'"
    
    data = []
    cursor = db.execute(query)
    temp = cursor.fetchall()
    for i in temp:
        data.append(i["Name"])
    db.close()
    return(data)

def new(name, message, db_name, stu):
    db_file_name = os.path.join(db_file, "{}".format(db_name))
    db = get_db(db_file_name)
    if stu == "stu":
        user = get_user()
    else:
        user = stu
    query = "INSERT INTO {} (Name, Message, Time) VALUES(?,?,?)".format("Chat" + user)
    now = datetime.now()  #gets current time
    current_time = now.strftime("%H:%M")
    db.execute(query, (name, message, current_time))

    db.commit()
    db.close()

def log_out():
    db_file_name = os.path.join(db_file, "Users.db")
    db = get_db(db_file_name)
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    print(f"IP Address: {ip_address}") 
    try:
        query = "UPDATE main.User SET Login = '0' WHERE Login = ?"
        db.execute(query, (ip_address,))
        db.commit()
        db.close()
    except:
        pass

def account_exist(Name):
    db_file_name = os.path.join(db_file, "Users.db")
    db = get_db(db_file_name)
    query = "SELECT Name, Password From User"
    cursor = db.execute(query)
    data = []
    temp = cursor.fetchall()
    pw = []
    for i in temp:
        data.append(i["Name"])
        pw.append(i["Password"])
    db.close()
    print("usernames", data)
    print("passwords", pw)
    for i in data:
        if i == Name:
            return True
    return False

def new_user(name, password, acc):
    db_file_name = os.path.join(db_file, "Users.db")
    db = get_db(db_file_name)
    tup1 = (name, acc, password)
    tup = str(tup1)
    query = "INSERT INTO User(Name, acc, Password) VALUES {}".format(tup)
    db.execute(query)
    db.commit()
    db.close()

#if not os.path.isfile("chat_with_prof.db"):
#    create_db(db_file_name)