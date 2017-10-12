# Code for reading the UniProt database .tsv (Look at uniprot-test.tab [Downloaded for all the Homo Sapiens Proteins]) and inputting isoforms and their names
import csv
from bs4 import BeautifulSoup
import requests
import re
from neo4j.v1 import GraphDatabase, basic_auth # Neo4j Driver: Download using pip "pip install neo4j-driver"

count = 0 # TO Keep track of the progress of the algorithm

def fastacatenate(proteinid): # Concatenation for the isoform FASTA website
    return 'http://www.uniprot.org/uniprot/' + proteinid + '.fasta'

def Graphdbatenate(protein, count, fasta): # Concatenation for setting the isoform FASTA identifier - Obtained from the UniProt Website
    return 'MATCH (n:Protein {identifier:"' + protein + '"}) SET n.isoform' + count + '_FASTA = "' + fasta + '" RETURN n'

def sourcatenate(protein, count, fasource): # Concatenation for the FASTA source
    return 'MATCH (n:Protein {identifier:"' + protein + '"}) SET n.isoform' + count + '_FASTA_Source = "' + fasource + '" RETURN n'

z = open('uniprot-homo+sap6.tab', 'r')

# Open the Graph Driver Session
driver = GraphDatabase.driver("bolt://neo4j-server/:7687", auth=basic_auth("username", "password"))
session = driver.session()

for line in z.readlines():
    
    cols = line.split('\t')
    if line:
        count = count + 1
        isoinfo = cols[8] # Column containing information about all the isoforms
        iso_split = isoinfo.split(';') # Split using the semicolon separators
        isoidarray = []
        isonumarray = []
        for i in range(len(iso_split)):
            if "IsoId=" in iso_split[i]: # Obtaining the Isoform IDs from the UniProt DB. They are found in the "IsoID=" splits
                e1 = iso_split[i].replace(' IsoId=', '')
                e2 = e1.replace(' ', '')
                isoidarray.append(e2)
            if "Name=" in iso_split[i]: # Obtaining the name of the Isoform. Thee are certain characters that the Neo4J DB does not accept, so I have filtered those out
                f1 = iso_split[i].replace(' Name=', '')
                f2 = f1.replace(' ', '')
                f3 = f2.replace('-', '')
                f4 = f3.replace('.', '_')
                f5 = re.sub('\{.*?\}','', f4)
                f6 = re.sub('\(.*?\)','', f5)
                f7 = re.sub('\[.*?\]','', f6)
                f8 = f7.replace("'", '_')
                f9 = f8.replace('+', '')
                f10 = f9.replace('*', '_')
                isonumarray.append(f10)
                
        print ("Count: " + str(count))
        
        if (len(isoidarray) > 1): # Obtaining and inputting the Isoform FASTAs and the Isoform FASTA source
            for j in range(len(isoidarray)):
                fsource = fastacatenate(isoidarray[j])
                print isoidarray[j]
                sstatement = sourcatenate(cols[0], isonumarray[j], fsource)
                print ("Isoform" + isonumarray[j])
                page = requests.get(fsource).text
                soup = BeautifulSoup(page, "lxml")
                for script in soup(["script", "style"]):
                    script.extract()    # rip it out
                # get text
                text = soup.get_text()
                # break into lines and remove leading and trailing space on each
                lines = (line.strip() for line in text.splitlines())

                for line in text.splitlines():
                    q = line
                    break
                print q
                isostatement = Graphdbatenate(cols[0], isonumarray[j], q)
                
   
                session.run(sstatement) # Run the input query for the FASTA entry
                session.run(isostatement)


session.close()
                    
