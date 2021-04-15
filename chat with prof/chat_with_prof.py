import sqlite3
from sqlite3 import Error


def connect_sql(name):
    try:
        conn = sqlite3.connect(name)
        print("connect successful")
        return(conn)
    except Error as e:
        return(e)


def read_data(conn):
    try:
        print("I")
        cursor = conn.execute("SELECT * FROM Chat")
        rows = cursor.fetchall()
        print(rows)
        for row in rows:
            print(row)
    except Error as e:
        return(e)


database_name = "chat_with_prof.db"
conn = connect_sql(database_name)
read_data(conn)
conn.close()
