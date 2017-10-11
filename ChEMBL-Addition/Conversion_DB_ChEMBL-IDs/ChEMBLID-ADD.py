# Algorithm for adding ChEMBL IDs to existing Compounds within SPOKE

from neo4j.v1 import GraphDatabase, basic_auth
import csv

driver = GraphDatabase.driver("bolt://neo4j-server", auth=basic_auth("Username", "Password")) # Neo4j server details left out for security purposes
session = driver.session()

def add_string(parameter1, parameter2):
    return "MATCH (n:Compound {identifier: '" + parameter1 +  "'})" + " SET n.chembl_id='" + parameter2 + "'" + " RETURN n.name"

with open('DB-TO-CHEMBL-PROGRAM.csv') as f:
  reader = csv.reader(f, delimiter=',')
  for line in reader:
      if line:
          dbid = line[0]
          chemblid = line[1]
          q = add_string(str(dbid), str(chemblid))
          print(q)  
          session.run(q)
            
session.close()
