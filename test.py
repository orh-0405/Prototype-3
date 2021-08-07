#import sqlite3
#def get_db(Dbname):
#    db = sqlite3.connect(Dbname)#problem should be check_same_thread = False
#    print("Opened database successfully")
#    db.row_factory = sqlite3.Row
#    return(db)
#
#db = get_db("uni_database_file/Data_car.db")
#
#print(db)
#db.close()
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")