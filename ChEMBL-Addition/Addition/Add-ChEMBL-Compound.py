# The ChEMBL database is massive (> 1.7 million compounds). For efficiency sake, I split the file into 10 other files using a regular split -l command [This entire sequence can definitely be automated using a bash-script]
# Refer to Sample-ChEMBL-Compounds.tsv for the file used to add the compounds to SPOKE
# Import the relevant packages
import csv
from neo4j.v1 import GraphDatabase, basic_auth # Neo4j-driver to interface python with the Neo4J MSGAP server

su = "false"

def matchcatenate(compound): # Concatenating the MATCH Neo4j command: This is used to make sure the compound does not already exist within the DrugBank Database previously added by Daniel Himmelstein
    return "MATCH (n) WHERE n.chembl_id = '" + compound + "' RETURN n.name"

def addsmiles(compound, smilesid): # Adding the Canonical SMILES as found in the ChEMBL database
    return "MATCH (n) WHERE n.chembl_id = '" + compound + "' SET n.canonical_smiles = '" + smilesid + "' RETURN n.name"

def addcmpd(compound, inchi, inchikey, smiles, pref_name, source): # Add the ChEMBL compound if it already doesn't exist in the SPOKE network
    return "CREATE (n:Compound{chembl_id: '" + compound + "', identifier: '" + compound + "', inchi: '" + inchi + "', inchikey: '" + inchikey + "', canonical_smiles: '" + smiles + "', pref_name: '" + pref_name + "', source: '" + source + "'}) RETURN n.identifier"

z = open('ChEMBL-SPOKE6.tsv', 'r') # Imported from the ChEMBL SQL db using a JOIN between the Molecule_dictionary and the Compound_structures tables

# Open the driver session using neo4j.v1
driver = GraphDatabase.driver("bolt://neo4jserver/:7687", auth=basic_auth("username", "password")) # Username, Password not included for security purposes
session = driver.session()

# Read each line of the document
for line in z.readlines():
    cols = line.split('\t')
    if line:
        su = "false"
        sfind = matchcatenate(cols[1])
        print sfind
        result = session.run(sfind)
        print "Passed: " + cols[1]
        for record in result:
            print "Got Here!"
            smilesadd = addsmiles(cols[1], cols[3])
            session.run(smilesadd)
            su = "true"
        if (su == "true"):
            print "true!"

        if (su == "false"):
            pref_name = ""
            if not (cols[2] == "\N"): # Certain columns had \N corresponding to the preferred compound name. In this case the name was not added, but the ChEMBL ID was still added along with the Compounds' structures
                pref_name = cols[2].replace("'", '"')
            else:
                pref_name = ""
            smiles = cols[3]
            inchi = cols[5]
            inchikey = cols[4]
            source = "https://www.ebi.ac.uk/chembl/compound/inspect/" + cols[1] # Concatenate the source with the ID for the URL
            scmpd = addcmpd(cols[1], inchi, inchikey, smiles, pref_name, source)
            session.run(scmpd)

        su = "false"

session.close() # Close session after finishing the addition of compounds
