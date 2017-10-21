from neo4j.v1 import GraphDatabase, basic_auth
import mysql.connector

driver = GraphDatabase.driver("bolt://127.0.0.1/:7687", auth=basic_auth("neo4j2", "neo4j2"))
session = driver.session()

cnx = mysql.connector.connect(user='root', password='')
cursor = cnx.cursor(buffered=True)

node_dict = {}
cursor.execute('USE SPOKE_Try_Sources;')
cursor.execute('CREATE TABLE Node_Keys_Sources (Key_ID varchar(200), Source_ID varchar(20), Node_Type varchar(100), Node_PK_ID varchar(20));')
cursor.execute('SELECT Node_PK_ID as nodid, Property_Key_Type as prop from Node_Props_Ref;')

def sqlatenate(tblname, key1, key2, key3, key4):
    return "INSERT INTO " + str(tblname) + " VALUES ('" + str(key1) + "', '" + str(key2) + "', '" + str(key3) + "', '" + str(key4) + "');"

for (nodid, prop) in cursor:
    node_dict.update({prop: nodid})

for k, v in node_dict.iteritems():
    print k, v

cursor.execute('SELECT Source_ID as srcid, Source_Name as srcname from Ref_Sources;')

src_dict = {}
for (srcid, srcname) in cursor:
    src_dict.update({srcname:srcid})

record = session.run('MATCH (n) where exists (n.source) UNWIND keys(n) as kl RETURN kl as key, n.uuid as uuid, n.source as src, labels(n) as lbl')

for line in record:
    nodid = node_dict[str(line["key"])]
    prop_id = str(line["uuid"]) + "|" + nodid
    t1 = str(line["lbl"]).replace("u'", '')
    t2 = t1.replace('[', '')
    t3 = t2.replace(']', '')
    t4 = t3.replace("'", '')
    sourceid = src_dict[str(line["src"])]
    cmd = sqlatenate("Node_Keys_Sources", prop_id, sourceid, t4.strip(), nodid)
    cursor.execute(cmd)
    print cmd
    #print prop_id, sourceid, t4.strip()

cnx.commit()
session.close()




