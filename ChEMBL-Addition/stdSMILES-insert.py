from neo4j.v1 import GraphDatabase, basic_auth

def concatenate(chemblid, stdsmiles):
    return 'MATCH (n:Compound) where n.chembl_id = "' + chemblid + '" set n.standardized_smiles = "' + stdsmiles + '"'

file = open('stdsmiles-atkins-all.csv', 'r')

for line in file:
    if line:
        cols = line.split(',')
        if not "None" in cols[1]:
            driver = GraphDatabase.driver("bolt://msgap1.ucsf.edu/:7687", auth=basic_auth("kbharat96", "tejas320"))
            session = driver.session()
            cmd = concatenate(cols[0], cols[2].strip())
            print cmd
            session.run(cmd)

session.close()
            
