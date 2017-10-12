# Making sure that all the ChEMBL IDs added from UniProt into SPOKE exist so that the Compound-Interacts-Protein edges can be easily added
from neo4j.v1 import GraphDatabase, basic_auth

def concatenate(pchembl):
    return 'MATCH (n:Protein) where n.chembl_id = "' + pchembl + '" return n.identifier as id'

f = open('tars-org-prot.tsv', 'r')
e = open('tars-notfound.txt', 'w+')

driver = GraphDatabase.driver("bolt://neo4j-server/:7687", auth=basic_auth("Username", "Password"))
session = driver.session()

for line in f.readlines():
    cols = line.split('\t')
    if line:
        su = "false"
        cmd = concatenate(cols[9])
        print cols[9]
        result = session.run(cmd)
        for record in result:
            su = "true"
            tmp = record["id"]
            print "Found!"
        result.consume()
        if (su == "false"):
            print "Not Found!" + str(cols[9])
            e.write(cols[9])
            e.write('\n')
        
