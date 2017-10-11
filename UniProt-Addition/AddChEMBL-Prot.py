# Script for adding ChEMBL IDs to Proteins within SPOKE
# This will help us form Compound-Interacts_With-Protein relationships
import csv
from neo4j.v1 import GraphDatabase, basic_auth

# Concatenated Neo4j Statement
def chemblatenate(protein, chembl):
    return 'MATCH (n:Protein {identifier:"' + protein + '"}) SET n.chembl_id = "' + chembl + '" RETURN n'

count = 0

driver = GraphDatabase.driver("bolt://neo4j-server/:7687", auth=basic_auth("Username", "Password")) # Username and Password excluded for security purposes
session = driver.session()

z = open('uniprot-all-chembl3.tab', 'r') # Contains information about the UniProt proteins along with their ChEMBL IDs
for line in z.readlines():
    cols = line.split('\t')
    if line:
        count = count + 1
        if cols[4] is not None: # Checking whether there exists a ChEMBL ID for a corresponding Protein ==> If there is, add the protein
            chemblid = cols[4].split(';') # Some cases where there are multiple ChEMBL IDs: we are trying to filter out those cases
            if (len(chemblid) > 2):
                act1id = cols[4].replace(';', ',') # Getting rid of extraneous SemiColons
                act2id = act1id.replace(' ', '')
                actid = act2id[:-1]
                print ("Multiple ChEMBL: " + actid)
            else:
                act1id = cols[4].replace(';', '')
                actid = act1id.replace(' ', '')
            actid = actid.rstrip("\n") # Make sure that another line does not get added on
            print actid # This helps track my progress in case the script has an error in the middle
            chemcmd = chemblatenate(cols[0], actid)
            print chemcmd
            session.run(chemcmd) # Run the input query for the ChEMBL ID entry

session.close()
