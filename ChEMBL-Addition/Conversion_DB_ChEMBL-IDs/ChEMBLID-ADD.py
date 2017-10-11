from neo4j.v1 import GraphDatabase, basic_auth
import csv

def add_string(parameter1, parameter2):
    return "MATCH (n:Compound {identifier: '" + parameter1 +  "'})" + " SET n.chembl_id='" + parameter2 + "'" + " RETURN n.name"

with open('DB-TO-CHEMBL-PROGRAM.csv') as f:
  reader = csv.reader(f, delimiter=',')
  for line in reader:
      if line:
          doid = line[0]
          chemblid = line[1]
          q = add_string(str(doid), str(chemblid))
          print(q)  
          driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=basic_auth("neo4j", "tejas320"))
#          driver = GraphDatabase.driver("bolt://msgap1.ucsf.edu:7687", auth=basic_auth("kbharat96", "tejas321"))
          session = driver.session()
          session.run(q)
          session.close()
