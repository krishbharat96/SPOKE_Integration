import requests
from bs4 import BeautifulSoup

## UniProt File Schema:
## ID,Name,Gene Name,GenBank Protein ID,GenBank Gene ID,UniProt ID,Uniprot Title,PDB ID,GeneCard ID,GenAtlas ID,HGNC ID,Species,Drug IDs

file = open('all-protein-targets.csv', 'r') # Downloaded from DrugBank Website
op_file = open('prot-output.csv', 'w+')
op_file.write('ProteinID,ProteinType,DrugBankID,DrugName,DrugGroup,Pharm_Action,Drug_Actions')
op_file.write('\n')

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
                   dact = c[4].text
                   print cols[0], 'target', dbid, dname, dgroup, dpharm_act, dact
                   op_file.write(str(cols[0]).strip() + ',target,' + str(dbid) + ',' + str(dname) + ',' + str(dgroup) + ',' + str(dpharm_act) + ',' + str(dact))
                   print str(cols[0]).strip() + ',target,' + str(dbid) + ',' + str(dname) + ',' + str(dgroup) + ',' + str(dpharm_act) + ',' + str(dact)
                   op_file.write('\n')

                   
               
               
        
