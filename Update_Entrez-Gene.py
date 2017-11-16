import pandas as pd
import gzip
from neo4j.v1 import GraphDatabase, basic_auth
import urllib
from gzip import GzipFile
import shutil

def vestige_gene_neo4j(geneid):
    return "MATCH (g:Gene) where g.identifier = " + str(geneid) + " SET g.vestige = True"

def update_gene_neo4j(geneid, name, desc, chrom):
    return 'MATCH (g:Gene) where g.identifier = ' + str(geneid) + ' SET g.name = "' + name + '", g.description = "' + desc + '", g.chromosome = "' + chrom + '"'

def add_gene_neo4j(geneid, name, desc, chrom, url):
    return 'CREATE (g:Gene) SET g.identifier = ' + str(geneid) + ', g.name = "' + name + '", g.description = "' + desc + '", g.chromosome = "' + chrom + '", g.url = "' + url + '", g.source = "Entrez Gene", g.license = "CC0 1.0"'

driver = GraphDatabase.driver("bolt://127.0.0.1/:7687", auth=basic_auth("neo4j", "neo4j2")) ## Change this for authentication
session = driver.session()

gene_keys = session.run("MATCH (g:Gene) where g.name contains '' UNWIND keys(g) as key_s RETURN distinct(key_s) as act_key")
keys_arr = []

for elem in gene_keys:
    keys_arr.append(str(elem["act_key"]))

init_string = "MATCH (gene:Gene) where gene.name contains '' return "
act_string = ""

for i in range(len(keys_arr)):
    if (i == 0):
        tmp = init_string
        new_str = "gene." + keys_arr[i] + " as " + keys_arr[i]
        act_string = tmp + new_str
    else:
        tmp_2 = act_string
        new_str = ", gene." + keys_arr[i] + " as " + keys_arr[i]
        act_string = tmp_2 + new_str

prev_genedb = session.run(act_string)
exists_gene_dict = {}
for rec in prev_genedb:
    ident = str(rec["identifier"])
    single_dict = {}
    for it in keys_arr:
        it_val = ""
        if (str(rec[it]) == "None"):
            it_val = "-"
        else:
            it_val = str(rec[it])
        single_dict.update({it:it_val})
    exists_gene_dict.update({ident:single_dict})

good = str(exists_gene_dict["4877"]["chromosome"])
print good
print exists_gene_dict

arr_exists_id = []
for k, v in exists_gene_dict.iteritems():
    arr_exists_id.append(str(v["identifier"]))

gene_url = 'ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz'
urllib.urlretrieve(gene_url, 'Homo_sapiens.gene_info.gz')

with gzip.open('Homo_sapiens.gene_info.gz', 'rb') as f_in, open('Homo_sapiens.gene_info', 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)

gene_df = pd.DataFrame.from_csv('Homo_sapiens.gene_info', sep='\t', header=0, index_col=None)
columns = ['#tax_id', 'GeneID', 'Symbol', 'chromosome', 'map_location', 'type_of_gene', 'description']
select_df = gene_df[columns]
select_df = select_df.rename(columns={'#tax_id':'tax_id'})
select_df = select_df.query("tax_id == 9606")
select_df = select_df.query("type_of_gene == 'protein-coding'") 
print len(select_df)

arr_new_id = []

for item, row in select_df.iterrows():
    arr_new_id.append(str(row["GeneID"]))
    

vestige = 0
vestige_arr = []

for item_ex in arr_exists_id:
    if item_ex not in arr_new_id:
        vestige = vestige + 1
        vestige_arr.append(item_ex)
        session.run(vestige_gene_neo4j(item_ex)).consume() 

new_add = 0
new_add_arr = []

for item_new in arr_new_id:
    if item_new not in arr_exists_id:
        new_add = new_add + 1
        new_add_arr.append(item_new)
##        print "New Item to be Added : " + item_new

update = 0
for it, rw in select_df.iterrows():
    if str(rw["GeneID"]) in new_add_arr:
        url = "http://identifiers.org/ncbigene/" + str(rw["GeneID"])
        session.run(add_gene_neo4j(str(rw["GeneID"]), str(rw["Symbol"]), str(rw["description"]), str(rw["chromosome"]), url)).consume()
    else:
        gene_id = str(rw["GeneID"])
        if (exists_gene_dict[gene_id]["name"] != str(rw["Symbol"])) or (exists_gene_dict[gene_id]["description"] != str(rw["description"])) or (exists_gene_dict[gene_id]["chromosome"] != str(rw["chromosome"])):
            update = update + 1
            print update_gene_neo4j(str(rw["GeneID"]), str(rw["Symbol"]), str(rw["description"]), str(rw["chromosome"]))
            session.run(update_gene_neo4j(str(rw["GeneID"]), str(rw["Symbol"]), str(rw["description"]), str(rw["chromosome"]))).consume()
            
                                                                                                    

print "Number_New_Added : " + str(new_add)
print "Number of Vestiges : " + str(vestige)
print "Number Updates : " + str(update)                                     
#print gene_df.head()

session.close()

