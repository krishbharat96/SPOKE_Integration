from neo4j.v1 import GraphDatabase, basic_auth
import csv

driver = GraphDatabase.driver("bolt://neo4j-server:7687", auth=basic_auth("Username", "Password"))
session = driver.session()

def add_string(parameter1, parameter2):
    return "MATCH (n:Disease {identifier: '" + parameter1 +  "'})" + " SET n.mesh_id='" + parameter2 + "'" + " RETURN n.name"

with open('Diseases_MESH.csv') as f:
  reader = csv.reader(f, delimiter=',')
  for line in reader:
      if line:
          doid = line[1]
          meshid = line[2]
          q = add_string(str(doid), str(meshid))
          print(q)  
          session.run(q)

session.close()

