import mysql.connector 
#  script to be run once ,just to create db
my_db= mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="  PASSWORD   "
)

my_cursor= my_db.cursor()
# my_cursor.execute("CREATE DATABASE todo_db")

my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print("name:",db)