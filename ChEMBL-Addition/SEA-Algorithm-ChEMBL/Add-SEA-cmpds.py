from neo4j.v1 import basic_auth, GraphDatabase
import csv
import time

driver = GraphDatabase.driver("bolt://msgap1.ucsf.edu/:7687", auth=basic_auth("kbharat96", "tejas320"))
session = driver.session()

record = session.run("MATCH (c:Compound)-[r:INTERACTS_CiP]-(p:Protein) RETURN c.chembl_id as cmpd, p.chembl_id as prot")
cp_arr = []
for rec in record:
    element = str(rec["cmpd"]) + "-" + str(rec["prot"])
    cp_arr.append(element)

# Name of Property Key --> ic50_values_chembl
# Boolean for Drug_Interaction --> False (drug_interaction: "False")

def create_prop_key(param):
    p1 = param.replace(" ", "")
    p2 = p1.lower()
    return p2


##def create_rel(p1, p2, p3, p4, p5):
##    retu

count_tot = 0
i = open("parsed_outfile_2.csv", "r")
dict_fin = {}
for line in i:
    cols = line.split(",")
    if line:
        count_tot = count_tot + 1
        split_id = cols[0].split("-")
        tar_id = split_id[0].strip()
        cmpd_id = split_id[1].strip()
        test_init = split_id[2].strip()
        test = create_prop_key(test_init) + "_values_chembl"

        if (count_tot%1000 == 0):
            print "Count Completed : " + str(count_tot)
        split_val = cols[1].split(";")
        arr_val = []
        for item in split_val:
            item_arr = item.split("|")
            element = item_arr[3].strip() + ";" + item_arr[2].strip()
            arr_val.append(element)
        
        uid_a = cmpd_id + "-"+ tar_id

        if uid_a in cp_arr:
            session.run("MATCH (c:Compound)-[r:INTERACTS_CiP]-(p:Protein) where c.chembl_id = '" + cmpd_id + "' and p.chembl_id = '" + tar_id + "' SET r." + test + " = " + str(arr_val))
            print "Present and Detected!", ("MATCH (c:Compound)-[r:INTERACTS_CiP]-(p:Protein) where c.chembl_id = '" + cmpd_id + "' and p.chembl_id = '" + tar_id + "' SET r." + test + " = " + str(arr_val))
        else:
            su = "false"
            cp_arr.append(uid_a)
            rec_2 = session.run("MATCH (c:Compound)-[r:INTERACTS_CiP]-(p:Protein) where c.chembl_id = '" + cmpd_id + "' and p.chembl_id = '" + tar_id + "' RETURN r.action_type as act")
            for elem in rec_2:
                su = "true"
                print "Got Here!"

            if (su == "true"):
                print "Ha Good!", ("MATCH (c:Compound)-[r:INTERACTS_CiP]-(p:Protein) where c.chembl_id = '" + cmpd_id + "' and p.chembl_id = '" + tar_id + "' SET r." + test + " = " + str(arr_val))
                session.run("MATCH (c:Compound)-[r:INTERACTS_CiP]-(p:Protein) where c.chembl_id = '" + cmpd_id + "' and p.chembl_id = '" + tar_id + "' SET r." + test + " = " + str(arr_val))
            else:
                print "sai", ("MATCH (c:Compound), (p:Protein) where c.chembl_id = '" + cmpd_id + "' and p.chembl_id = '" + tar_id + "' CREATE (c)-[r:INTERACTS_CiP]->(p) SET r." + test + " = " + str(arr_val) + ", r.action_type = 'UNKNOWN', r.drug_interaction = 'false', r.source = 'ChEMBL', r.license = 'CC BY-SA 3.0'") 
                session.run("MATCH (c:Compound), (p:Protein) where c.chembl_id = '" + cmpd_id + "' and p.chembl_id = '" + tar_id + "' CREATE (c)-[r:INTERACTS_CiP]->(p) SET r." + test + " = " + str(arr_val) + ", r.action_type = 'UNKNOWN', r.drug_interaction = 'false', r.source = 'ChEMBL', r.license = 'CC BY-SA 3.0'")
                
        
##        split_test_results = (cols[1].strip()).split("|")
##        test_bound = split_test_results[2].strip()
##        test_rel = split_test_results[3].strip()


session.close()
        
