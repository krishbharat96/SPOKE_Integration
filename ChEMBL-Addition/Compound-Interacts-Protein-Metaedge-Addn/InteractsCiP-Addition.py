# Script for adding Compound-SINGLE PROTEIN edges gathered from the ChEMBL Database
from neo4j.v1 import GraphDatabase, basic_auth

def concatenate(pchembl, cchembl, actype): # Concatenated query for adding the respective fields. pchembl is the protein's chembl ID (added in UniProt-Addition folder)
    return 'MATCH (p:Protein), (c:Compound) WHERE p.chembl_id = "' + pchembl + '" AND c.chembl_id = "' + cchembl + '" CREATE (c)-[r:INTERACTS_CiP]->(p) SET r.action_type = "' + actype + '", r.source = "ChEMBL", r.license = "CC BY-SA 3.0"'

f = open('tars-org-prot-copy.tsv', 'r')
e = open('tars-notfound.txt', 'w')

driver = GraphDatabase.driver("bolt://neo4j-server/:7687", auth=basic_auth("Username", "Password"))
session = driver.session()

for line in f.readlines():
    cols = line.split('\t')
    if line:
        var = cols[4]
        if (cols[4] == '\N'): # \N = NULL, so replace those with "UNKNOWN" as Cypher does not respond well to "\N" datapoints
            var = 'UNKNOWN'
        else:
            var = cols[4]
        cmd = concatenate(cols[9].strip(), cols[11].strip(), var)
        print cmd
        session.run(cmd).consume() # Consume the query: sometimes data leaks tend to happen if the query is not consumed. Could affect processing power and speed

session.close()
