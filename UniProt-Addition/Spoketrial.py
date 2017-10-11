from neo4j.v1 import GraphDatabase, basic_auth
driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=basic_auth("neo4j", "tejas320"))
session = driver.session()
session.run("MATCH (n:Disease {identifier: 'DOID:4606'})" "SET n.mesh_id = 'D001650'" "RETURN n.name") 
session.close()
