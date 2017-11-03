# Code to parse DrugBank .xml file for Drug-Interacts_With-Protein Data
# .xml file can be found in the Downloads section of: http://www.drugbank.ca
# Readily available extension for DrugBank users to use

import xml.etree.ElementTree as ET

o = open('write-db-prot.csv', 'w+') # Output filename

xml_file = open('full_database.xml', 'r')
tree = ET.parse(xml_file)
root = tree.getroot()

ns = '{http://www.drugbank.ca}'

## Schema: DrugBankID|DrugName|UniProtID|DrugBank_ProtID|Category|ActionType
## Outputs overall file into a '|' delimited file [Schema shown above^]

for drug in root.findall(ns + "drug"):
    drugbank_id = drug.findtext(ns + "drugbank-id[@primary='true']")
    drug_name = drug.findtext(ns + "name")
    type_drug = ['enzyme', 'target', 'carrier', 'transporter'] # Change this array if you only want certain categories
    for typ in type_drug:
        for drug_t in drug.findall(ns + typ + "s/" + ns + typ):
            act_input = ""
            for act in drug_t.findall(ns + "actions/" + ns + "action"):
                if not (act_input == ""):
                    tmp = act_input + ";" + act.text
                    act_input = tmp
                else:
                    act_input = act.text

            targid = drug_t.findtext(ns + "id")
            
            proteinid = ""
            protein = drug_t.find(ns + "polypeptide")
            if not (protein == {}) and protein is not None:
                if "id" in protein.attrib:
                    proteinid = protein.attrib["id"]
                

            print drugbank_id + "|" + drug_name + "|" + proteinid + "|" + targid + "|" + typ + "|" + act_input
            o.write(drugbank_id.encode('utf-8') + "|" + drug_name.encode('utf-8') + "|" + proteinid.encode('utf-8') + "|" + targid.encode('utf-8') + "|" + typ.encode('utf-8') + "|" + act_input.encode('utf-8'))
            o.write("\n")


