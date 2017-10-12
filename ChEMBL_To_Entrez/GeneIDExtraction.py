import csv
from bs4 import BeautifulSoup
import requests
import re

e = open('ChEMBLtoENSEMBL.txt', "w+")

def commacatenate(param1, param2):
    return param1 + "," + param2

with open('targets.txt') as f:
    reader = csv.reader(f, delimiter = '\t')
    for line in reader:
        if line:
            #print(line[1])
            print(line[5])
            page = requests.get('https://www.ebi.ac.uk/chembl/target/inspect/' + line[5]).text
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
                #var = commacatenate(line[5], i)
                #print(var1)
                #print(var)
            
                
                
