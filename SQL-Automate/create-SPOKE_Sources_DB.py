import mysql.connector

cnx = mysql.connector.connect(user='root', password='')
cursor = cnx.cursor(buffered=True)

cursor.execute("CREATE DATABASE SPOKE_Try_Sources;")

cnx.commit()
cnx.close()
