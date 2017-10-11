# Attempt at using the webpages to import the UniProt Accession ID.
# Found later that UniProt provides the ChEMBL ID option with each protein ID
# ChEMBL Target/Protein IDs were eventually added using the UniProt feature

import csv
from bs4 import BeautifulSoup
import requests
import re

#e = open('ChEMBLtoUniProt.txt', "w+")
def commacatenate(param1, param2):
    return param1 + "," + param2

#q is a var that is F if the UniProt/canSAR ID is found
#The row after canSAR displays the ID so this is an important step
#Preliminary Code: canSAR displays only work for certain UniProt IDs --> Not for all existing ones
#Refer to Working-ChEMBL-UniProt.py for working code -- Use this code as skeleton
e = open('ChEMBL&Prot.txt', "w")
e.write("Start of Document")
e.write('\n')
q = "NF"

with open('targets.txt') as f:
    reader = csv.reader(f, delimiter = '\t')
    for line in reader:
        if line:
            #print(line[1])
            #print(line[5])
            page = requests.get('https://www.ebi.ac.uk/chembl/target/inspect/' + line[5]).text
            soup = BeautifulSoup(page, "lxml")
            table = soup.find('table')
            UniProt = re.compile('UniProt')
            for row in table.find_all("a"):
                if (q == "F"):
                    UniChem = commacatenate(line[5], row.text)
                    print(UniChem)
                    e.write(UniChem)
                    e.write('\n')
                if UniProt.match(row.text):
                    q = "F"
                    continue
                else:
                    q = "NF"               
            #ID = UniProt[0].nextSibling
            #print ID.text
