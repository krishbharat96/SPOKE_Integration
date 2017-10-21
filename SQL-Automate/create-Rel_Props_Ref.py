from neo4j.v1 import GraphDatabase, basic_auth
import mysql.connector

driver = GraphDatabase.driver("bolt://127.0.0.1/:7687", auth=basic_auth("neo4j2", "neo4j2"))
session = driver.session()

cnx = mysql.connector.connect(user='root', password='')
cursor = cnx.cursor(buffered=True)

def sqlatenate(tblname, key1, key2):
    return "INSERT INTO " + str(tblname) + " (Rel_PK_ID, Property_Key_Type) VALUES ('" + str(key1) + "', '" + str(key2) + "');"

cursor.execute('USE SPOKE_Try_Sources;')
cursor.execute('CREATE TABLE Rel_Props_Ref(Rel_PK_ID varchar(20), Property_Key_Type varchar(100));')
src_array = []
src_n_records = session.run('MATCH ()-[r]-() UNWIND keys(r) as kl RETURN DISTINCT(kl) as actkeys')
for record in src_n_records:
    src_array.append(record['actkeys'])
    id1 = "R" + str(str(len(src_array)).zfill(4))
    cmd = sqlatenate('Rel_Props_Ref', id1, record['actkeys'])
    print cmd
    cursor.execute(cmd)

cnx.commit()
cnx.close()
session.close()
