from neo4j.v1 import GraphDatabase, basic_auth
import mysql.connector

driver = GraphDatabase.driver("bolt://127.0.0.1/:7687", auth=basic_auth("neo4j2", "neo4j2"))
session = driver.session()

cnx = mysql.connector.connect(user='root', password='')
print "Connected!"
cursor = cnx.cursor()

def sqlatenate(tblname, key1, key2):
    return "INSERT INTO " + str(tblname) + " (Node_PK_ID, Property_Key_Type) VALUES ('" + str(key1) + "', '" + str(key2) + "');"

cursor.execute('USE SPOKE_Try_Sources;')
print "Used!"
cursor.execute('CREATE TABLE Node_Props_Ref(Node_PK_ID varchar(20), Property_Key_Type varchar(100));')
print "Table Created!"
src_array = []
src_n_records = session.run('MATCH (n) UNWIND keys(n) as kl RETURN DISTINCT(kl) as actkeys')
print "Session Running!"
for record in src_n_records:
    src_array.append(record['actkeys'])
    id1 = "N" + str(str(len(src_array)).zfill(4))
    cmd = sqlatenate('Node_Props_Ref', id1, record['actkeys'])
    print cmd
    cursor.execute(cmd)

cnx.commit()
cnx.close()
session.close()
