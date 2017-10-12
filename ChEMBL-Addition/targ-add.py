from neo4j.v1 import GraphDatabase, basic_auth

def concatenate(pchembl, cchembl, actype):
    return 'MATCH (p:Protein), (c:Compound) WHERE p.chembl_id = "' + pchembl + '" AND c.chembl_id = "' + cchembl + '" CREATE (c)-[r:INTERACTS_CiP]->(p) SET r.action_type = "' + actype + '", r.source = "ChEMBL", r.license = "CC BY-SA 3.0"'

f = open('tars-org-prot-copy.tsv', 'r')
e = open('tars-notfound.txt', 'w')

driver = GraphDatabase.driver("bolt://msgap1.ucsf.edu/:7687", auth=basic_auth("kbharat96", "tejas320"))
session = driver.session()

for line in f.readlines():
    cols = line.split('\t')
    if line:
        su = "false"
        var = cols[4]
        if (cols[4] == '\N'):
            var = 'UNKNOWN'
        else:
            var = cols[4]
        cmd = concatenate(cols[9].strip(), cols[11].strip(), var)
        print cmd
        session.run(cmd).consume()

session.close()
