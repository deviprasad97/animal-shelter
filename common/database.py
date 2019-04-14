import mysql.connector

mydb = mysql.connector.connect(
  host="18.223.184.82",
  user="root",
  passwd="root"
)

print(mydb)
