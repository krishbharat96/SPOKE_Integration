# File that parses ENSEMBL website followed by the HGNC website and converts Ensembl IDs converted from ChEMBL ID to the Gene ID
# This was for the previous version of SPOKE in which there were edges that connected Genes directly to compounds
# In the new version, the Compound interaction edges connect to proteins
# This implementation was mainly used to connect ChEMBL target IDs to Entrez Gene IDs

from bs4 import BeautifulSoup
import requests
import re
import csv
import fileinput

def commacatenate3(param1, param2, param3):
    return param1 + "," + param2 + "," + param3

def commacatenate2(param1, param2):
    return param1 + "," + param2

with open("FoundCE.txt") as f: # File containing list of ChEMBL and Ensembl IDs (resembles ChEMBL-Ensembl-Entrez.csv found in this folder but does not have the Entrez IDs)
    reader = csv.reader(f, delimiter = ",")
    for line in reader:
        if line:
            print line[1]
            page = requests.get('http://www.ensembl.org/Homo_sapiens/Gene/Summary?g=' + line[1]).text # First parse ENSEMBL site for HGNC ID
            soup = BeautifulSoup(page, "html5lib")
            GeneID = soup.body.find_all(text=re.compile('HGNC'))
            print(GeneID[1])
            if GeneID[0] is not None:
                page2 = requests.get('http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=' + GeneID[1]).text # Then parse the HGNC site for the Entrez Gene ID
                soup2 = BeautifulSoup(page2, "html5lib")
                EntrezGeneID = soup2.body.find_all(text=re.compile('Entrez Gene:'))
                nextSib = EntrezGeneID[0].nextSibling
                print "Entrez Gene:" + nextSib.text
