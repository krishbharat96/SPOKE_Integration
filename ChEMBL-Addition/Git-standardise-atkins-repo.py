# Code for standardizing SMILES identifiers obtained from ChEMBL
from standardiser import standardise # This package can be installed from: https://github.com/flatkinson/standardiser
from rdkit import Chem

def concatenate(chembl, smiles1, smiles2):
    return chembl + ',' + smiles1 + ',' + smiles2

su = ""

file = open('stdsmiles-atkins.csv', 'w')
afile = open('all-static-copy.csv', 'r')
bfile = open('exceptions-atkins.txt', 'w')

for line in afile:
    if line:
        cols = line.split(',')
       
        if not "None" in cols[1]:
            mol = Chem.MolFromSmiles(cols[1])
            try:
                p1 = standardise.run(mol)
                parent = Chem.MolToSmiles(p1)
            except (standardise.StandardiseException, TypeError): # Except Errors and write "error" in place of the code (these were inputted into SPOKE)
                #bfile.write(cols[0] + ',' + cols[1])
                #bfile.write('\n')
                parent = "error"
                print "Error!"
                bfile.write(concatenate(cols[0], str(cols[1].strip()), str(parent)))
                bfile.write('\n')
            
        else:
            parent = ""
        l = concatenate(cols[0], str(cols[1].strip()), str(parent))
        print l
        file.write(l)
        file.write('\n')
