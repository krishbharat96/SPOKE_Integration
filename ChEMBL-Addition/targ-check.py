from neo4j.v1 import GraphDatabase, basic_auth

def concatenate(pchembl):
    return 'MATCH (n:Protein) where n.chembl_id = "' + pchembl + '" return n.identifier as id'

f = open('tars-org-prot.tsv', 'r')
e = open('tars-notfound.txt', 'w+')

driver = GraphDatabase.driver("bolt://msgap1.ucsf.edu/:7687", auth=basic_auth("kbharat96", "tejas320"))
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
        
