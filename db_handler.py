import os.path
import sqlite3

curr_dir = os.path.dirname(__file__)
#print(curr_dir)
 ##abs path
## ^ working directory may not be same directory as python file
## sometimes, creating a db might not have it in the same directory
## thus use cur dir to generate file name

def get_db():
    db_name = 'Practical_car.db'
    db_file_name = os.path.join(curr_dir, db_name)
    db = sqlite3.connect(db_file_name, check_same_thread=False) #db, db3, sqlite, sqlite3
    print("Opened database successfully")#;
    db.row_factory = sqlite3.Row
    return db