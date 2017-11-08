# Adding Compound-Protein relationships pulled out of DrugBank to SPOKE
import requests
from bs4 import BeautifulSoup
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://msgap1.ucsf.edu/:7687", auth=basic_auth("kbharat96", "tejas320"))
session = driver.session()

## UniProt File Schema:
## ID,Name,Gene Name,GenBank Protein ID,GenBank Gene ID,UniProt ID,Uniprot Title,PDB ID,GeneCard ID,GenAtlas ID,HGNC ID,Species,Drug IDs

file = open('write-db-prot_4.csv', 'r') # Created using DrugBank Website

# Schema of Document created: 'ProteinID,ProteinType,DrugBankID,DrugName,DrugGroup,Pharm_Action,Drug_Actions'
# All identifiers pulled from DrugBank are in the DB Format

def cat(protid, dbid, dbaction):
    return "MATCH (c:Compound), (p:Protein) WHERE c.identifier = '" + dbid + "' and p.identifier = '" + protid + "' CREATE (c)-[r:INTERACTS_CiP]->(p) SET r.source = 'DrugBank', r.action_type = '" + dbaction + "', r.license = 'CC BY-ND 3.0'" 

record_cip = session.run("MATCH (c:Compound)-[r:INTERACTS_CiP]->(p:Protein) return c.identifier as cmpd, c.chembl_id as chembl, p.identifier as prot")
record_db = session.run("MATCH (c:Compound) where c.name contains '' and exists (c.drugbank_id) return c.identifier as id")

db_exists = []
for id_db in record_db:
    db_exists.append(id_db["id"])

print db_exists

full_arr = []

for lin1 in record_cip:
    ln = lin1["cmpd"] + "-" + lin1["prot"]
    full_arr.append(ln)
    print ln
print full_arr

# Divide up into 2 categories: relationships that already exist within SPOKE that have DB classifiers for compounds or relationships that have ChEMBL classifiers for Compounds
# In case a relationship already exists (from ChEMBL) do not add a rel from DrugBank to SPOKE
# In case a protein/compound id does not exist within SPOKE (but is still found in the file), do not add that particular relationship. Chances are some of these compound-protein relationships are not for humans (ie the Protein is not a Homo sapiens protein)

e = open('error_act.csv', 'w+')
for line in file.readlines():
    cols = line.split("|")
    if line:
        if cols[0].strip() in db_exists:
            lnog = cols[0].strip() + "-" + cols[1].strip()
            if lnog in full_arr: 
                print "Present:DrugBank " + lnog
            else:
                full_arr.append(lnog)
                if (cols[4].strip() == ""):
                    up = "UNKNOWN"
                else:
                    up = str(cols[4].upper())
                cmd = cat(cols[1].strip(), cols[0].strip(), up.strip())
                session.run(cmd)
                print cmd
        else:
            if not (cols[5].strip() == ""):
                lnog_chem = cols[5].strip() + "-" + cols[1].strip()
                if lnog_chem in full_arr:
                    print "Present:ChEMBL " + lnog_chem
                else:
                    full_arr.append(lnog_chem)
                    if (cols[4].strip() == ""):
                        up = "UNKNOWN"
                    else:
                        up = str(cols[4].upper())
                    cmd = cat(cols[1].strip(), cols[5].strip(), up.strip())
                    session.run(cmd)
                    print cmd
            else:
                e.write(line.strip())
                e.write("\n")
                    
session.close()
