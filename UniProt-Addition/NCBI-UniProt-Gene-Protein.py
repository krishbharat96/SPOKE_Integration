import csv
from bs4 import BeautifulSoup
import requests
import re
# The approach below definitely works! However, UniProt already provides this option within their webpage - That approach was used instead.
# Algorithm for gathering information about the Proteins and their associated Gene IDs from the NCBI webpage
e = open("NCBIPage-New.txt", "w+")
with open("Multiple-UniProt.txt") as f:
    reader = csv.reader(f, delimiter = ',')
    for line in reader:
        protid = line[0]
        print(protid)
        e.write(protid)
        e.write('\n')
        for i in range(len(line) - 1):
            if not (i == 0):
                q = "NF"
                q2 = "NF"
                page = requests.get('https://www.ncbi.nlm.nih.gov/gene/?term=' + line[i] + '#').text
                soup = BeautifulSoup(page, "html5lib")
                for script in soup(["script", "style"]):
                    script.extract()    # rip it out

                # get text
                text = soup.get_text()

                # break into lines and remove leading and trailing space on each
                lines = (line.strip() for line in text.splitlines())

                for line3 in lines:
                    if (q == "F"):
                        #print line3
                        name = line3
                        actual_name = name.replace('provided by HGNC', '')
                        #print actual_name
                    if (q2 == "F"):
                        #print line3
                        nname = line3
                        actual_nname = nname.replace('provided by HGNC', '')
                        #print actual_nname

                    if "Symbol" in line3:
                        q2 = "F"
                    else:
                        q2 = "NF"
                    
                    if "Full Name" in line3:
                        q = "F"
                    else:
                        q = "NF"

                print('  ' + line[i] + ': ' + actual_nname + ' ' + actual_name)
                e.write('  ' + line[i] + ': ' + actual_nname + ' ' + actual_name)
                e.write('\n')
                  
            #nextSib = UniProt[0].nextSibling
            #print (nextSib.text)
