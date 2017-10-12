from bs4 import BeautifulSoup
import requests
import re
import csv
import fileinput

def commacatenate3(param1, param2, param3):
    return param1 + "," + param2 + "," + param3

def commacatenate2(param1, param2):
    return param1 + "," + param2

with open("FoundCE.txt") as f:
    reader = csv.reader(f, delimiter = ",")
    for line in reader:
        if line:
            #e = open('writepage.txt', "w+")
            print line[1]
            page = requests.get('http://www.ensembl.org/Homo_sapiens/Gene/Summary?g=' + line[1]).text
            soup = BeautifulSoup(page, "html5lib")
            GeneID = soup.body.find_all(text=re.compile('HGNC'))
            #e.write(str(page))
            print(GeneID[1])
            #print(GeneID[1])
            if GeneID[0] is not None:
                page2 = requests.get('http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=' + GeneID[1]).text
                soup2 = BeautifulSoup(page2, "html5lib")
                EntrezGeneID = soup2.body.find_all(text=re.compile('Entrez Gene:'))
                nextSib = EntrezGeneID[0].nextSibling
                print "Entrez Gene:" + nextSib.text
