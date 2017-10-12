# Code for parsing the ChEMBL website for the Ensembl Gene ID
# Note that this was mainly done for the previous SPOKE implementation in which there were only edges directly connecting Compounds to Genes
# Refer to UniProt-Addition folder for more details regarding this protein node and edge addition

import csv
from bs4 import BeautifulSoup # HTML parsing package
import requests
import re

e = open('ChEMBLtoENSEMBL.txt', "w+")

def commacatenate(param1, param2):
    return param1 + "," + param2

with open('targets.txt') as f:
    reader = csv.reader(f, delimiter = '\t')
    for line in reader:
        if line:
            print(line[5])
            page = requests.get('https://www.ebi.ac.uk/chembl/target/inspect/' + line[5]).text # Parsing the ChEMBL site for the Ensembl ID
            soup = BeautifulSoup(page, "lxml")
            Ensembl = soup.body.find_all(text=re.compile('ENSG'))
            if Ensembl:
                var = commacatenate(line[5], Ensembl[0])
                print(var)
                e.write(Ensembl[0])
                e.write('\n')
            else:
                varnf = commacatenate(line[5], "Not Found")
                e.write("Not Found")
                e.write('\n')
            
                
                
