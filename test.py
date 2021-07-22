import sqlite3
def get_db(Dbname):
    db = sqlite3.connect(Dbname)#problem should be check_same_thread = False
    print("Opened database successfully")
    db.row_factory = sqlite3.Row
    return(db)

db = get_db("uni_database_file/Data_car.db")

print(db)
db.close()