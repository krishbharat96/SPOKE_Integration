# Converting DrugBank ID to ChEMBL ID :: Added to a csv file which was used to insert the IDs back to SPOKE
import csv
from bs4 import BeautifulSoup
import requests
import re
import fileinput

def commacatenate(param1, param2):
    return param1 + "," + param2

with open('DB-To-ChemBL-Conversion3.csv') as f:
    reader = csv.reader(f, delimiter = ',')
    for line in reader:
        if (line[1] == "Not Found"):
            #print(line[1])
            page = requests.get('https://www.drugbank.ca/drugs/' + line[0]).text
            soup = BeautifulSoup(page)
            Chembl = soup.body.find_all(text=re.compile('CHEMBL'))
            for i in Chembl:
                var1 = commacatenate(line[0], line[1])
                var2 = commacatenate(line[0], i)
                #print(var1)
                print(var2)
                for line in fileinput.FileInput("DB-To-ChemBL-Conversion3.csv",inplace=1):
                    line = line.replace(var1, var2).rstrip()
                    print line
