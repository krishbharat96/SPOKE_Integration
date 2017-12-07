import pandas as pd
import gzip
from neo4j.v1 import GraphDatabase, basic_auth
import urllib
from gzip import GzipFile
import shutil
import csv
import re
import time

def does_isokey_exist(arr):
    su = "false"
    for item in arr:
        if "isoform" in item:
            su = "true"
    if (su == "false"):
        return False
    else:
        return True

def extract_iso(arr):
    result = []
    for item in arr:
        if "isoform" in item:
            result.append(item)
    return result

def process_iso(iso_string):
    split = iso_string.split(";")
    iso_name = []
    iso_id = []
    iso_seq = []
    iso_canonical = []
    
    for item in split:
        if "Name=" in item:
            it_n = item.split('Name=', 1)[-1]
            iso_name.append(it_n)
        if "IsoId=" in item:
            it_id = item.split("IsoId=", 1)[-1]
            iso_id.append(it_id)
        if "Sequence=" in item:
            it_seq = item.split("Sequence=", 1)[-1]
            iso_seq.append(it_seq)

    seq_index = 0
    for seq in range(len(iso_seq)):
        if "Displayed" in iso_seq[seq]:
            seq_index = seq
    iso_canonical = [iso_name[seq_index], iso_id[seq_index], seq_index]
    
    iso_dict = dict()
    iso_dict.update({"Names": iso_name, "IDs": iso_id, "Canonical": iso_canonical})
    return iso_dict

def FASTA_maker(db_uniprot, prot_id, entry_name, prot_name, gene_names, org, is_isoform, isoform_name, iso_id, pe, sv):
    # FASTA format: >db|UniqueIdentifier|EntryName ProteinName OS=OrganismName[ GN=GeneName]PE=ProteinExistence SV=SequenceVersion
    fasta = ""
    gene_arr = gene_names.split(" ")
    act_gene = gene_arr[0]
    act_prot = re.sub(r'\([^()]*\)', '', prot_name).strip()
    if (is_isoform == "true"):
        fasta = ">" + str(db_uniprot) + "|" + str(prot_id) + "|" + str(entry_name) + " " + str(act_prot) + " " + "OS=" + str(org) +  " GN=" + str(act_gene) + " PE=" + pe + " SV=" + sv
    else:
        fasta = ">" + str(db_uniprot) + "|" + str(iso_id) + "|" + str(entry_name) + " Isoform " + str(isoform_name) + " of " + str(act_prot) + " OS=" + str(org) + " GN=" + str(act_gene)
    return fasta

def create_iso_key(iso_dict, db_uniprot, gene_names, prot_name, prot_id, entry_name, org, pe, sv):
    canonical_num = iso_dict["Canonical"][2]
    fasta_arr = []
    fastasource_arr = []
    iscanonical = []
    name_arr = []
    
    for i in range(len(iso_dict["Names"])):
        fasta = ""
        fasta_src = ""
        if (i == canonical_num):
            isoname = iso_dict["Names"][i]
            fasta = FASTA_maker(db_uniprot, prot_id, entry_name, prot_name, gene_names, org, "true", "", "", pe, sv)
            fasta_source = "http://www.uniprot.org/uniprot/" + str(prot_id) + ".fasta"
            fasta_arr.append(fasta)
            fastasource_arr.append(fasta_source)
            iscanonical.append("true")
            name_arr.append(isoname)
        else:
            iso_id = iso_dict["IDs"][i]
            isoname = iso_dict["Names"][i]
            fasta = FASTA_maker(db_uniprot, prot_id, entry_name, prot_name, gene_names, org, "false", isoname, iso_id, pe, sv)
            fasta_source = "http://www.uniprot.org/uniprot/" + str(iso_id) + ".fasta"
            fasta_arr.append(fasta)
            fastasource_arr.append(fasta_source)
            iscanonical.append("false")
            name_arr.append(isoname)

    iso_full_arr = []
    for n in range(len(fasta_arr)):
        iso_string = "Name:Isoform " + name_arr[n] + "~FASTA:" + fasta_arr[n] + "~FASTA_Source:" + fastasource_arr[n] + "~Is_Canonical:" + iscanonical[n]
        iso_full_arr.append(iso_string)

    return iso_full_arr

def vestige_prot_neo4j(protid):
    return "MATCH (p:Protein) where p.identifier = '" + str(protid) + "' SET p.vestige = True"

def add_prot_neo4j(prot_id, prot_name, prot_desc, prot_reviewed, prot_isoform, prot_chembl_id):
    prot_url = "http://www.uniprot.org/uniprot/" + str(prot_id)
    if (prot_chembl_id == "None") and not (prot_isoform == "None"):
        return "CREATE (p:Protein) SET p.identifier = '" + prot_id + "', p.name = '" + prot_name + "'" + ', p.description = "' + prot_desc + '"' + ", p.reviewed = '" + prot_reviewed + "', p.isoform = " + str(prot_isoform) + ", p.url = '" + prot_url + "', p.license = 'CC BY-ND 3.0', p.source = 'UniProt'"
    elif (prot_isoform == "None") and not (prot_chembl_id == "None"):
        return "CREATE (p:Protein) SET p.identifier = '" + prot_id + "', p.name = '" + prot_name + "'" + ', p.description = "' + prot_desc + '"' + ", p.reviewed = '" + prot_reviewed + "', p.url = '" + prot_url +  "', p.chembl_id = '" + prot_chembl_id + "', p.license = 'CC BY-ND 3.0', p.source = 'UniProt'"
    elif (prot_chembl_id == "None") and (prot_isoform == "None"):
        return "CREATE (p:Protein) SET p.identifier = '" + prot_id + "', p.name = '" + prot_name + "'" + ', p.description = "' + prot_desc + '"' + ", p.reviewed = '" + prot_reviewed + "', p.url = '" + prot_url +  "', p.license = 'CC BY-ND 3.0', p.source = 'UniProt'"
    else:
        return "CREATE (p:Protein) SET p.identifier = '" + prot_id + "', p.name = '" + prot_name + "'" + ', p.description = "' + prot_desc + '"' + ", p.reviewed = '" + prot_reviewed + "', p.isoform = " + str(prot_isoform) + "', p.chembl_id = '" + prot_chembl_id + "', p.url = '" + prot_url + "', p.license = 'CC BY-ND 3.0', p.source = 'UniProt'"

def update_prot_neo4j(prot_id, prot_name, prot_desc, prot_reviewed, prot_isoform, prot_chembl_id):
    syntax = ""
    if (prot_isoform == "None") and (prot_chembl_id == "None"):
        syntax = "MATCH (p:Protein) where p.identifier = '" + prot_id + "' SET p.name = '" + prot_name + "'" + ', p.description = "' + prot_desc + '"' + ", p.reviewed = '" + prot_reviewed + "' REMOVE p.isoform, p.chembl_id"
    elif (prot_isoform == "None") and not (prot_chembl_id == "None"):
        syntax = "MATCH (p:Protein) where p.identifier = '" + prot_id + "' SET p.name = '" + prot_name + "'" + ', p.description = "' + prot_desc + '"' + ", p.chembl_id = '" + prot_chembl_id + "', p.reviewed = '" + prot_reviewed + "' REMOVE p.isoform"
    elif (prot_chembl_id == "None") and not (prot_isoform == "None"):
        syntax = "MATCH (p:Protein) where p.identifier = '" + prot_id + "' SET p.name = '" + prot_name + "'" + ', p.description = "' + prot_desc + '"' + ", p.isoform = " + str(prot_isoform) + ", p.reviewed = '" + prot_reviewed + "' REMOVE p.chembl_id"
    else:
        syntax = "MATCH (p:Protein) where p.identifier = '" + prot_id + "' SET p.name = '" + prot_name + "'" + ', p.description = "' + prot_desc + '"' + ", p.isoform = " + str(prot_isoform) + ", p.chembl_id = '" + prot_chembl_id + "', p.reviewed = '" + prot_reviewed + "'"       
    return syntax

def pe_converter(pe_string):
    num = 0
    if "protein level" in pe_string.lower():
        num = 1
    elif "transcript level" in pe_string.lower():
        num = 2
    elif "homology" in pe_string.lower():
        num = 3
    elif "predicted" in pe_string.lower():
        num = 4
    else:
        num = 5
    return str(num)

# Link for downloading .tsv UniProt File
print "Downloading UniProt Database..."
url = """
http://www.uniprot.org/uniprot/?sort=&desc=&compress=yes&query=&fil=organism:%22Homo%20sapiens%20(Human)%20[9606]%22&format=tab&force=yes&columns=id,entry%20name,reviewed,protein%20names,genes,organism,length,go(biological%20process),go(molecular%20function),database(ChEMBL),comment(ALTERNATIVE%20PRODUCTS),feature(ALTERNATIVE%20SEQUENCE),version(sequence),existence
"""
urllib.urlretrieve(url, 'full_prot.gz')
with gzip.open('full_prot.gz', 'rb') as f_in, open('full_prot.tsv', 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)
print "Downloaded!"

driver = GraphDatabase.driver("bolt://127.0.0.1/:7687", auth=basic_auth("neo4j", "neo4j2")) ## Change this for authentication
session = driver.session()

prot_info = session.run("MATCH (p:Protein) WHERE not exists (p.vestige) return p.name as name, p.identifier as id, p.description as desc, p.reviewed as rev, p.isoform as iso, p.chembl_id as chembl")
prot_dict = dict()
arr_exists = []

for rec in prot_info:
    id_prot = str(rec["id"])
    name_prot = str(rec["name"])
    desc_prot = str(rec["desc"])
    rev_prot = str(rec["rev"])
    chembl_prot = str(rec["chembl"])
    
    if (str(rec["iso"]) == "None"):
        iso = "None"
    else:
        iso = sorted(rec["iso"])
    
    arr_exists.append(id_prot)
        
    single_prot_dict = {"identifier":id_prot, "name":name_prot, "iso_array":iso, "desc":desc_prot, "rev":rev_prot, "chembl":chembl_prot}
    prot_dict.update({id_prot:single_prot_dict})
    
arr_new = []
prot_df = pd.read_csv('full_prot.tsv', sep = '\t', dtype=object, index_col=None)
for it_1, rw_1 in prot_df.iterrows():
    arr_new.append(str(rw_1["Entry"]))

it_sub = list(set(arr_exists) - set(arr_new))
count_vest = 0
for item_ex in it_sub:
    print vestige_prot_neo4j(item_ex)
    session.run(vestige_prot_neo4j(item_ex))
    count_vest = count_vest + 1

add_arr = list(set(arr_new) - set(arr_exists))

cnt_add = 0
cnt_iso_update = 0
cnt_update = 0

print "Adding new proteins ..."
for it, rw in prot_df.iterrows():
    prot_rev = "Unreviewed, From TrEMBL"
    db = "tr"
    if (str(rw["Status"]) == "reviewed"):
        prot_rev = "Reviewed, From SwissProt"
        db = "sp"
    else:
        prot_rev = "Unreviewed, From TrEMBL"
        db = "tr"

    prot_chembl = "None"
    if not (str(rw["Cross-reference (ChEMBL)"]) == "nan"):
        prot_chembl = str(rw["Cross-reference (ChEMBL)"]).replace(";", "").strip()
    
    if str(rw["Entry"]) in add_arr:
        cnt_add = cnt_add + 1
        iso = ""
        if not str(rw["Alternative products (isoforms)"]) == "nan":
             iso = create_iso_key(process_iso(str(rw["Alternative products (isoforms)"])), db, str(rw["Gene names"]), str(rw["Protein names"]), str(rw["Entry"]), str(rw["Entry name"]), str(rw["Organism"]).replace(" (Human)", ""), pe_converter(str(rw["Protein existence"])), str(rw["Version (sequence)"]))
        else:
            iso = "None" # Could change this to displaying information about the one and only isoform

        prot_id = str(rw["Entry"])
        prot_name = str(rw["Entry name"])
        prot_desc = str(rw["Protein names"])

        # print add_prot_neo4j(prot_id, prot_name, prot_desc, prot_rev, iso, prot_chembl)
        session.run(add_prot_neo4j(prot_id, prot_name, prot_desc, prot_rev, iso, prot_chembl))

print "Proteins Added!"
time.sleep(2)
print "Updating protein data ..."
for it1, rw1 in prot_df.iterrows():
    prot_rev = "Unreviewed, From TrEMBL"
    db = "tr"
    if (str(rw1["Status"]) == "reviewed"):
        prot_rev = "Reviewed, From SwissProt"
        db = "sp"
    else:
        prot_rev = "Unreviewed, From TrEMBL"
        db = "tr"

    prot_chembl = "None"
    if not (str(rw1["Cross-reference (ChEMBL)"]) == "nan"):
        prot_chembl = str(rw1["Cross-reference (ChEMBL)"]).replace(";", "").strip()
    
    if not (str(rw1["Entry"])) in add_arr:
        iso_2 = "None"
        if not (str(rw1["Alternative products (isoforms)"]) == "nan"):               
            iso_2 = sorted(create_iso_key(process_iso(str(rw1["Alternative products (isoforms)"])), db, str(rw1["Gene names"]), str(rw1["Protein names"]), str(rw1["Entry"]), str(rw1["Entry name"]), str(rw1["Organism"]).replace(" (Human)", ""), pe_converter(str(rw1["Protein existence"])), str(rw1["Version (sequence)"])))

        prev_dict = prot_dict[str(rw1["Entry"])]
        current_dict = {"identifier":str(rw1["Entry"]), "name":str(rw1["Entry name"]), "iso_array":iso_2, "desc":str(rw1["Protein names"]), "rev":prot_rev, "chembl":prot_chembl}
        if not (prev_dict == current_dict):
            cnt_update = cnt_update + 1
            session.run(update_prot_neo4j(str(rw1["Entry"]), str(rw1["Entry name"]), str(rw1["Protein names"]), prot_rev, iso_2, prot_chembl))
            #print update_prot_neo4j(str(rw1["Entry"]), str(rw1["Entry name"]), str(rw1["Protein names"]), prot_rev, iso_2, prot_chembl)
print "Updated Protein Data! Look below for stats regarding this update : "

print "Number Updated : " + str(cnt_update)
print "Number Added : " + str(cnt_add)
print "Number Vestiges : " + str(count_vest)

