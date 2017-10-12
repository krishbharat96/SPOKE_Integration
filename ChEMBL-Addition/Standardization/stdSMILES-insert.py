# Code for inserting Standardized SMILES identifiers into SPOKE
from neo4j.v1 import GraphDatabase, basic_auth

def concatenate(chemblid, stdsmiles):
    return 'MATCH (n:Compound) where n.chembl_id = "' + chemblid + '" set n.standardized_smiles = "' + stdsmiles + '"'

driver = GraphDatabase.driver("bolt:neo4j-server:7687", auth=basic_auth("Username", "Password"))
session = driver.session()

file = open('stdsmiles-atkins-all.csv', 'r') # Sample file can be found within this folder: std-sample.csv

for line in file:
    if line:
        cols = line.split(',')
        if not "None" in cols[1]: # Some instances in which there were no SMILES identifiers from ChEMBL, and some nodes do not have SMILES on SPOKE - have to filter them out
            cmd = concatenate(cols[0], cols[2].strip())
            print cmd
            session.run(cmd)

session.close()
            
