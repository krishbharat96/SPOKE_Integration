from neo4j.v1 import GraphDatabase, basic_auth
import mysql.connector

driver = GraphDatabase.driver("bolt://127.0.0.1/:7687", auth=basic_auth("neo4j2", "neo4j2"))
session = driver.session()

cnx = mysql.connector.connect(user='root', password='')
cursor = cnx.cursor()

def sqlatenate(tblname, key1, key2):
    return "INSERT INTO " + str(tblname) + " (Source_ID, Source_Name) VALUES ('" + str(key1) + "', '" + str(key2) + "');"
su = "False"
cursor.execute('USE SPOKE_Try_Sources;')
cursor.execute('CREATE TABLE Ref_Sources (Source_ID varchar(50), Source_Name varchar(200));')
cursor.execute('SELECT count(*) FROM Ref_Sources;')

l = ""
for line in cursor:
    l1 = str(line).replace('(', '')
    l2 = l1.replace(')', '')
    l = l2.replace(',', '')
count = int(l)

src_array = []
src_n_records = session.run('MATCH ()-[r]-() UNWIND r.sources as sl RETURN DISTINCT(sl) as actsrc')
for record in src_n_records:
    su = "False"
    cmd1 = "SELECT 1 from Ref_Sources WHERE Ref_Sources.Source_Name = '" + str(record["actsrc"]) + "';"
    print cmd1
    cursor.execute(cmd1)
    for rec in cursor:
        su = "True"

    if (su == "False"):
        src_array.append(record['actsrc'])
        id1 = "S" + str(str(count + len(src_array)).zfill(4))
        cmd = sqlatenate('Ref_Sources', id1, record['actsrc'])
        print cmd
        print record['actsrc']
        cursor.execute(cmd)

cnx.commit()
cnx.close()
session.close()
