from neo4j.v1 import GraphDatabase, basic_auth
import csv

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
          driver = GraphDatabase.driver("bolt://msgap1.ucsf.edu:7687", auth=basic_auth("kbharat96", "tejas321"))
          session = driver.session()
          session.run(q)
          #session.close()

