from neo4j.v1 import GraphDatabase, basic_auth
import mysql.connector

driver = GraphDatabase.driver("bolt://127.0.0.1/:7687", auth=basic_auth("neo4j2", "neo4j2"))
session = driver.session()

cnx = mysql.connector.connect(user='root', password='')
cursor = cnx.cursor()

rel_dict = {}
cursor.execute('USE SPOKE_Try_Sources;')
cursor.execute('SELECT Rel_PK_ID as rel, Property_Key_Type as prop from Rel_Props_Ref;')

def sqlatenate(tblname, key1, key2, key3, key4):
    return "INSERT INTO " + str(tblname) + " VALUES ('" + str(key1) + "', '" + str(key2) + "', '" + str(key3) + "', '" + str(key4) + "');"

def propenate(param1, param2):
    return str(param1) + "|" + str(param2)

for (rel, prop) in cursor:
    rel_dict.update({prop: rel})

for k, v in rel_dict.iteritems():
    print k, v

cursor.execute('SELECT Source_ID as srcid, Source_Name as srcname from Ref_Sources;')

src_dict = {}
for (srcid, srcname) in cursor:
    src_dict.update({srcname:srcid})

record = session.run('MATCH ()-[r]-() where exists (r.sources) UNWIND keys(r) as kl RETURN kl as key, r.uuid as uuid, r.sources as src, type(r) as typ')

for line in record:
    prop_id = str(line["uuid"]) + "|" + rel_dict[str(line["key"])]
    t1 = str(line["typ"]).replace("u'", '')
    t2 = t1.replace('[', '')
    t3 = t2.replace(']', '')
    t4 = t3.replace("'", '')
    
    s1 = str(line["src"]).replace("u'", '')
    s2 = s1.replace('[', '')
    s3 = s2.replace(']', '')
    s4 = s3.replace("'", '')
    s5 = s4.replace(", ", ',')
    sourc_arr = s5.split(',')
    
    for i in sourc_arr:
        cmd = sqlatenate("Rel_Keys_Sources", prop_id, str(src_dict[str(i)]).strip(), t4.strip(), rel_dict[str(line["key"])])
        print cmd
        cursor.execute(cmd)
    #sourceid = src_dict[str(s4)]

cnx.commit()
session.close()




