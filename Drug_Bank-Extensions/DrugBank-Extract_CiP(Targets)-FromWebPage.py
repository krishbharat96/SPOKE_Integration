# Script for extracting information directly from DrugBank website in order to add more Compounds-:INTERACTS_WITH-Protein Edges

import requests
from bs4 import BeautifulSoup

## UniProt File Schema:
## ID,Name,Gene Name,GenBank Protein ID,GenBank Gene ID,UniProt ID,Uniprot Title,PDB ID,GeneCard ID,GenAtlas ID,HGNC ID,Species,Drug IDs

file = open('all-protein-targets.csv', 'r') # Downloaded from DrugBank Website
op_file = open('prot-cmpd-output.csv', 'w+')
op_file.write('ProteinID|ProteinType|DrugBankID|DrugName|DrugGroup|Pharm_Action|Drug_Actions')
op_file.write('\n')

def elim_split(param):
    p1 = param.replace('<td>', '')
    p2 = p1.replace('</td>', '')
    p3 = p2.replace('</strong><strong class="badge">', ';')
    p4 = p3.replace('<strong class="badge">', '')
    p5 = p4.replace('</strong>', '')
    return p5.strip()


for line in file:
    cols = line.split(',')
    if line:
        if (cols[11] == 'Human'):            
            url = 'https://www.drugbank.ca/biodb/polypeptides/' + str(cols[0]).strip()
            page = requests.get(url).text
            soup = BeautifulSoup(page, "lxml")
            drug_tbl = soup.find_all('table')[1]

            for row in drug_tbl.find_all('tr'):
               c = row.find_all('td')
               if (len(c) > 0):
                   dbid = c[0].text
                   dname = c[1].text
                   dgroup = c[2].text
                   dpharm_act = c[3].text
                   dact = elim_split(str(c[4].encode('utf-8')))
                   print cols[0], 'target', dbid, dname, dgroup, dpharm_act, dact
                   op_file.write(str(cols[0]).strip() + '|target|' + dbid.encode('utf-8') + '|' + dname.encode('utf-8') + '|' + dgroup.encode('utf-8') + '|' + dpharm_act.encode('utf-8') + '|' + dact.encode('utf-8'))
                   op_file.write('\n')
                   
               
               
        
